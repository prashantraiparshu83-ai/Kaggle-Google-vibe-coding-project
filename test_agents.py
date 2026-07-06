import unittest
import os
import shutil
import json
from agents_cli.security import PIIScrubber, LocalEncryptor
from agents_cli.mcp import MCPServerConnection
from agents_cli.agents import (
    DiagnosticAgent,
    CurriculumAgent,
    AnalysisAgent,
    RemediationAgent,
    AssessmentAgent,
    FeedbackAgent,
    ReportAgent
)
from agents_cli.session import SessionManager, SESSIONS_DIR

class TestEducationGapAgent(unittest.TestCase):

    def setUp(self):
        # Setup temporary session key and folder cleanup
        self.password = "test-encryption-key-123!"
        self.scrubber = PIIScrubber()
        self.encryptor = LocalEncryptor(self.password)
        
        # Clear out test sessions directory if exists
        if os.path.exists(SESSIONS_DIR):
            shutil.rmtree(SESSIONS_DIR)
        os.makedirs(SESSIONS_DIR, exist_ok=True)

    def tearDown(self):
        if os.path.exists(SESSIONS_DIR):
            shutil.rmtree(SESSIONS_DIR)

    def test_pii_scrubber(self):
        # Email & Phone scrubbing
        text = "Contact student John at john.doe@school.edu or call 123-456-7890."
        scrubbed = self.scrubber.scrub(text)
        self.assertNotIn("john.doe@school.edu", scrubbed)
        self.assertNotIn("123-456-7890", scrubbed)
        self.assertIn("[ANONYMIZED_EMAIL]", scrubbed)
        self.assertIn("[ANONYMIZED_PHONE]", scrubbed)

        # Custom keywords (e.g., student name)
        self.scrubber.add_keyword("John Doe")
        text_with_name = "The student's name is John Doe."
        scrubbed_name = self.scrubber.scrub(text_with_name)
        self.assertNotIn("John Doe", scrubbed_name)
        self.assertIn("[ANONYMIZED_NAME]", scrubbed_name)

    def test_encryption_decryption(self):
        secret_message = "This is a confidential student diagnostic session log."
        encrypted = self.encryptor.encrypt(secret_message)
        self.assertNotEqual(secret_message, encrypted)
        
        decrypted = self.encryptor.decrypt(encrypted)
        self.assertEqual(secret_message, decrypted)

        # Verify integrity tamper protection checks
        tampered = encrypted[:-5] + "AAAAA"
        with self.assertRaises(ValueError):
            self.encryptor.decrypt(tampered)

    def test_mcp_connection(self):
        conn = MCPServerConnection()
        with self.assertRaises(ConnectionError):
            conn.get_curriculum("AP Physics 1")
            
        conn.connect()
        curr = conn.get_curriculum("AP Physics 1")
        self.assertIn("standards", curr)
        self.assertEqual(curr["title"], "AP Physics 1: Algebra-Based Course & Exam Description")
        
        diags = conn.get_diagnostic_questions("AP Physics 1")
        self.assertTrue(len(diags) > 0)
        self.assertEqual(diags[0]["id"], "app1_q1")

    def test_pipeline_sequential_state_and_agents(self):
        # Complete sequential execution run mock
        manager = SessionManager(self.password)
        session_id = manager.create_session()
        state = manager.load_session(session_id)
        
        # Test Step 1: Goal
        diag_agent = DiagnosticAgent()
        state = diag_agent.process(
            state,
            subject="AP Physics 1",
            level="Grade 11",
            target="Score a 5 on Exam",
            milestones="4 weeks",
            student_name="Alice Smith",
            student_email="alice@school.edu"
        )
        self.assertEqual(state["step"], 1)
        manager.save_session(session_id, state)
        
        # Test Step 2: Analyze (Standards/Questions Fetch)
        conn = MCPServerConnection()
        curr_agent = CurriculumAgent(conn)
        state = curr_agent.process(state)
        self.assertEqual(state["step"], 2)
        self.assertEqual(len(state["diagnostic_questions"]), 3)
        manager.save_session(session_id, state)
        
        # Test out-of-order execution attempt (e.g. running Step 4 directly)
        remed_agent = RemediationAgent(conn)
        with self.assertRaises(ValueError):
            remed_agent.process(state) # Throws since state is step 2, needs step 3.

        # Test Step 3: Weak Topics Isolation
        # Simulate student answers: 1 correct, 2 incorrect (q2 and q3 wrong)
        student_answers = {
            "app1_q1": "g * sin(θ)", # Correct
            "app1_q2": "ω",          # Wrong (Correct is ω / 2)
            "app1_q3": "Unchanged"   # Wrong (Correct is Eightfold)
        }
        anal_agent = AnalysisAgent()
        state = anal_agent.process(state, student_answers)
        self.assertEqual(state["step"], 3)
        self.assertEqual(state["diagnostic_score"], "1/3")
        self.assertEqual(len(state["weak_topics"]), 2)
        self.assertIn("Unit 7: Torque and Rotational Motion", state["weak_topics"])
        self.assertIn("Unit 3: Circular Motion and Gravitation", state["weak_topics"])
        manager.save_session(session_id, state)
        
        # Test Step 4: Study Plan Formulation
        state = remed_agent.process(state)
        self.assertEqual(state["step"], 4)
        self.assertEqual(len(state["study_plan"]), 2)
        self.assertEqual(state["study_plan"][0]["topic"], "Unit 7: Torque and Rotational Motion")
        manager.save_session(session_id, state)
        
        # Test Step 5: Quiz Generation
        assess_agent = AssessmentAgent()
        state = assess_agent.process(state)
        self.assertEqual(state["step"], 5)
        self.assertEqual(len(state["quiz_questions"]), 2)
        self.assertEqual(state["quiz_questions"][0]["id"], "quiz_p2") # Rotational
        self.assertEqual(state["quiz_questions"][1]["id"], "quiz_p3") # Circular/Gravitation
        manager.save_session(session_id, state)
        
        # Test Step 6: Feedback & Mastery update
        # Quiz answers: 2 correct (100% mastery)
        quiz_answers = {
            "quiz_p2": "6.0 N·m",
            "quiz_p3": "Quartered"
        }
        feed_agent = FeedbackAgent()
        state = feed_agent.process(state, quiz_answers)
        self.assertEqual(state["step"], 6)
        self.assertEqual(state["quiz_score"], "2/2")
        self.assertEqual(state["mastery_level"], "100.0%")
        manager.save_session(session_id, state)
        
        # Test Step 7: Final Scrubbed Report
        rep_agent = ReportAgent()
        state = rep_agent.process(state)
        self.assertEqual(state["step"], 7)
        
        report = state["final_report"]
        self.assertIn("academic_metrics", report)
        self.assertIn("system_audit", report)
        
        # Verify PII scrubbing on final report JSON structure
        # Verify the raw names/emails are not leakage points
        report_str = json.dumps(report)
        self.assertNotIn("Alice Smith", report_str)
        self.assertNotIn("alice@school.edu", report_str)

if __name__ == "__main__":
    unittest.main()
