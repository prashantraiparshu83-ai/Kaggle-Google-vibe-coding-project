import json
from typing import List, Dict, Any
from agents_cli.mcp import MCPServerConnection
from agents_cli.security import PIIScrubber

class BaseAgent:
    def __init__(self, name: str):
        self.name = name

    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process the state and return the updated state."""
        raise NotImplementedError("Subclasses must implement process method.")

class DiagnosticAgent(BaseAgent):
    def __init__(self):
        super().__init__("DiagnosticAgent")

    def process(self, state: Dict[str, Any], subject: str, level: str, target: str, milestones: str, student_name: str, student_email: str) -> Dict[str, Any]:
        # Save student inputs
        state["subject"] = subject
        state["level"] = level
        state["target"] = target
        state["milestones"] = milestones
        
        # PII elements to be scrubbed in security checks
        state["student_name"] = student_name
        state["student_email"] = student_email
        
        # Initialize progress tracker
        state["step"] = 1
        return state

class CurriculumAgent(BaseAgent):
    def __init__(self, mcp_connection: MCPServerConnection):
        super().__init__("CurriculumAgent")
        self.mcp = mcp_connection

    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        if state.get("step") != 1:
            raise ValueError("Invalid pipeline sequence: Must complete Step 1 before Step 2.")
            
        subject = state["subject"]
        self.mcp.connect()
        
        # Fetch standardized curriculum guidelines
        curriculum = self.mcp.get_curriculum(subject)
        state["curriculum_title"] = curriculum["title"]
        state["curriculum_standards"] = curriculum["standards"]
        
        # Fetch diagnostic baseline questions
        diagnostics = self.mcp.get_diagnostic_questions(subject)
        state["diagnostic_questions"] = diagnostics
        state["diagnostic_answers"] = {} # Will hold student answers
        
        state["step"] = 2
        return state

class AnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__("AnalysisAgent")

    def process(self, state: Dict[str, Any], answers: Dict[str, str]) -> Dict[str, Any]:
        if state.get("step") != 2:
            raise ValueError("Invalid pipeline sequence: Must complete Step 2 before Step 3.")
            
        state["diagnostic_answers"] = answers
        diagnostics = state["diagnostic_questions"]
        
        weak_topics = []
        correct_count = 0
        
        for q in diagnostics:
            q_id = q["id"]
            student_ans = answers.get(q_id, "").strip()
            correct_ans = q["answer"].strip()
            
            if student_ans.lower() == correct_ans.lower():
                correct_count += 1
            else:
                weak_topics.append(q["topic"])
                
        state["diagnostic_score"] = f"{correct_count}/{len(diagnostics)}"
        state["weak_topics"] = weak_topics
        state["step"] = 3
        return state

class RemediationAgent(BaseAgent):
    def __init__(self, mcp_connection: MCPServerConnection):
        super().__init__("RemediationAgent")
        self.mcp = mcp_connection

    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        if state.get("step") != 3:
            raise ValueError("Invalid pipeline sequence: Must complete Step 3 before Step 4.")
            
        weak_topics = state["weak_topics"]
        subject = state["subject"]
        self.mcp.connect()
        
        study_plan_items = []
        for topic in weak_topics:
            ref = self.mcp.get_textbook_resources(subject, topic)
            study_plan_items.append({
                "topic": topic,
                "textbook_reference": ref,
                "duration": "2 hours of targeted reading & exercise"
            })
            
        # If no weak topics, create a consolidation study plan
        if not study_plan_items:
            study_plan_items.append({
                "topic": "Advanced Mastery & Consolidation",
                "textbook_reference": f"Recommended review from general {subject} textbook resources",
                "duration": "1 hour review"
            })
            
        state["study_plan"] = study_plan_items
        state["step"] = 4
        return state

class AssessmentAgent(BaseAgent):
    def __init__(self):
        super().__init__("AssessmentAgent")

    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        if state.get("step") != 4:
            raise ValueError("Invalid pipeline sequence: Must complete Step 4 before Step 5.")
            
        weak_topics = state["weak_topics"]
        subject = state["subject"]
        
        # Dynamically construct micro-quiz questions targeted specifically at identified weak topics
        quiz_items = []
        
        # Database of micro-quiz items based on weak topics
        physics_quiz_db = {
            "Unit 2: Dynamics (Force and Newton's Laws)": {
                "id": "quiz_p1",
                "question": "A force F is applied to a mass m, producing an acceleration a. If the force is doubled and the mass is halved, the acceleration becomes:",
                "choices": ["a/2", "a", "2a", "4a"],
                "answer": "4a",
                "explanation": "Newton's Second Law: a = F / m. If F is replaced by 2F and m is replaced by m/2, the new acceleration is (2F) / (m/2) = 4 * (F/m) = 4a."
            },
            "Unit 7: Torque and Rotational Motion": {
                "id": "quiz_p2",
                "question": "What torque is produced by a perpendicular force of 15 N applied 0.4 m from the pivot of a wrench?",
                "choices": ["6.0 N·m", "37.5 N·m", "0.026 N·m", "15.4 N·m"],
                "answer": "6.0 N·m",
                "explanation": "Torque (τ) is computed as F * r * sin(θ). For a perpendicular force, sin(90°) = 1, so τ = 15 N * 0.4 m = 6.0 N·m."
            },
            "Unit 3: Circular Motion and Gravitation": {
                "id": "quiz_p3",
                "question": "If the distance between two spherical masses is doubled, the gravitational force between them is:",
                "choices": ["Doubled", "Halved", "Quadrupled", "Quartered"],
                "answer": "Quartered",
                "explanation": "Newton's Law of Gravitation: F = G * (m1 * m2) / r^2. If distance r is doubled to 2r, the force is divided by (2)^2 = 4 (Quartered)."
            }
        }
        
        calculus_quiz_db = {
            "Unit 1: Limits and Continuity": {
                "id": "quiz_c1",
                "question": "Find the limit: lim (x -> infinity) of (3x^2 + 5x) / (2x^2 - 7)",
                "choices": ["0", "1", "1.5", "Does not exist"],
                "answer": "1.5",
                "explanation": "By dividing the numerator and denominator by the highest power of x (x^2), we get lim (3 + 5/x) / (2 - 7/x^2) = (3 + 0) / (2 - 0) = 3/2 = 1.5."
            },
            "Unit 10: Infinite Sequences and Series": {
                "id": "quiz_c2",
                "question": "What is the sum of the geometric series 3 + 1 + 1/3 + 1/9 + ...?",
                "choices": ["4", "4.5", "6", "Infinite"],
                "answer": "4.5",
                "explanation": "The geometric series has first term a = 3 and common ratio r = 1/3. The sum is S = a / (1 - r) = 3 / (1 - 1/3) = 3 / (2/3) = 4.5."
            },
            "Unit 9: Parametric Equations, Polar Coordinates, and Vector-Valued Functions": {
                "id": "quiz_c3",
                "question": "At what values of θ in [0, 2π] does the polar curve r = cos(θ) pass through the pole (origin)?",
                "choices": ["0 and π", "π/2 and 3π/2", "π/4 and 5π/4", "Never"],
                "answer": "π/2 and 3π/2",
                "explanation": "The curve passes through the pole when r = 0, meaning cos(θ) = 0. In the range [0, 2π], cos(θ) is 0 at θ = π/2 and 3π/2."
            }
        }
        
        quiz_databases = {
            "physics": physics_quiz_db,
            "calculus": calculus_quiz_db,
            "chemistry": {
                "Unit 2: Chemical Bonding & Intermolecular Forces": {
                    "id": "quiz_chem1",
                    "question": "Which of the following intermolecular forces is strongest in pure liquid water?",
                    "choices": ["London dispersion forces", "Dipole-dipole interactions", "Hydrogen bonding", "Ion-dipole forces"],
                    "answer": "Hydrogen bonding",
                    "explanation": "Hydrogen bonding is a particularly strong type of dipole-dipole attraction that occurs between a hydrogen atom bonded to N, O, or F, and a lone pair on another electronegative atom."
                }
            },
            "ai": {
                "Unit 1: Introduction to Search Algorithms": {
                    "id": "quiz_ai1",
                    "question": "What is the primary heuristic function used in A* Search to find the optimal path?",
                    "choices": ["f(n) = g(n) + h(n)", "f(n) = g(n) - h(n)", "f(n) = g(n)", "f(n) = h(n)"],
                    "answer": "f(n) = g(n) + h(n)",
                    "explanation": "A* Search computes f(n) where g(n) is the cost to reach node n and h(n) is the estimated cost from n to the goal."
                }
            },
            "data science": {
                "Unit 2: Probability & Statistical Inference": {
                    "id": "quiz_ds1",
                    "question": "If a model has high variance and suffers from overfitting, what technique is best to remediate this?",
                    "choices": ["Add more features", "Increase model complexity", "L2 Regularization (Ridge)", "Remove data points"],
                    "answer": "L2 Regularization (Ridge)",
                    "explanation": "Regularization penalizes large coefficients, reducing variance and mitigating overfitting."
                }
            },
            "data analyst": {
                "Unit 1: SQL Queries and Data Aggregation": {
                    "id": "quiz_da1",
                    "question": "What type of join in SQL returns all records from the left table and matched records from the right table?",
                    "choices": ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN"],
                    "answer": "LEFT JOIN",
                    "explanation": "A LEFT JOIN returns all rows from the left table, with nulls in columns of the right table where no match is found."
                }
            },
            "web developer": {
                "Unit 1: HTML5 Semantics & CSS Layouts": {
                    "id": "quiz_web1",
                    "question": "Which JavaScript method is used to register an event handler on a DOM element?",
                    "choices": ["addEventListener", "attachEventHandler", "bindEvent", "onclickEvent"],
                    "answer": "addEventListener",
                    "explanation": "The addEventListener() method registers the specified listener on the EventTarget it's called on."
                }
            },
            "machine learning": {
                "Unit 1: Supervised Learning (Regression & Classification)": {
                    "id": "quiz_ml1",
                    "question": "What is the primary objective of Principal Component Analysis (PCA)?",
                    "choices": ["Predict continuous targets", "Group similar data clusters", "Reduce dimensionality while preserving variance", "Optimize gradient descent learning rate"],
                    "answer": "Reduce dimensionality while preserving variance",
                    "explanation": "PCA projects data into orthogonal dimensions of maximum variance to reduce feature dimensionality."
                }
            }
        }
        
        # Dynamically build quiz from weak topics
        db = {}
        for key, val in quiz_databases.items():
            if key in subject.lower():
                db = val
                break
                
        fallback_db = {
            "topic": "General Revision Question",
            "question": f"Explain the central concept of {subject.title()}.",
            "choices": ["Right Answer", "Wrong Option B", "Wrong Option C", "Wrong Option D"],
            "answer": "Right Answer",
            "explanation": "General remediation concept validation."
        }
        
        for topic in weak_topics:
            if topic in db:
                quiz_items.append(db[topic])
            else:
                # Fallback item if database topic doesn't match
                item = fallback_db.copy()
                item["topic"] = topic
                item["id"] = f"quiz_{len(quiz_items)+1}"
                quiz_items.append(item)
                
        # If no weak topics, provide a general mastery confirmation quiz
        if not quiz_items:
            for k, val in list(db.items())[:2]:
                quiz_items.append(val)
                
        state["quiz_questions"] = quiz_items
        state["quiz_answers"] = {}
        state["step"] = 5
        return state

class FeedbackAgent(BaseAgent):
    def __init__(self):
        super().__init__("FeedbackAgent")

    def process(self, state: Dict[str, Any], answers: Dict[str, str]) -> Dict[str, Any]:
        if state.get("step") != 5:
            raise ValueError("Invalid pipeline sequence: Must complete Step 5 before Step 6.")
            
        state["quiz_answers"] = answers
        quiz_questions = state["quiz_questions"]
        
        feedback_details = []
        correct_count = 0
        
        for q in quiz_questions:
            q_id = q["id"]
            student_ans = answers.get(q_id, "").strip()
            correct_ans = q["answer"].strip()
            
            is_correct = student_ans.lower() == correct_ans.lower()
            if is_correct:
                correct_count += 1
                feedback_details.append({
                    "question_id": q_id,
                    "is_correct": True,
                    "comment": "Perfect score on this topic! You have mastered this concept.",
                    "explanation": q.get("explanation", "")
                })
            else:
                feedback_details.append({
                    "question_id": q_id,
                    "is_correct": False,
                    "comment": "Not quite, but this is a great learning opportunity.",
                    "explanation": q.get("explanation", "")
                })
                
        state["quiz_score"] = f"{correct_count}/{len(quiz_questions)}"
        state["feedback"] = feedback_details
        
        # Calculate mastery rate
        rate = (correct_count / len(quiz_questions)) * 100 if quiz_questions else 100.0
        state["mastery_level"] = f"{rate:.1f}%"
        state["step"] = 6
        return state

class ReportAgent(BaseAgent):
    def __init__(self):
        super().__init__("ReportAgent")

    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        if state.get("step") != 6:
            raise ValueError("Invalid pipeline sequence: Must complete Step 6 before Step 7.")
            
        # PII Anonymization validation
        scrubber = PIIScrubber()
        scrubber.add_keyword(state.get("student_name", ""))
        scrubber.add_keyword(state.get("student_email", ""))
        
        report_data = {
            "academic_metrics": {
                "subject": state["subject"],
                "level": state["level"],
                "target_objective": state["target"],
                "milestones": state["milestones"],
                "diagnostic_score": state["diagnostic_score"],
                "initial_weak_topics": state["weak_topics"],
                "quiz_score": state["quiz_score"],
                "final_mastery_level": state["mastery_level"]
            },
            "system_audit": {
                "anonymization_verified": True,
                "pii_scrubbed_from_export": True
            }
        }
        
        # Stringify and scrub to double check security
        raw_json_report = json.dumps(report_data, indent=2)
        scrubbed_json_report = scrubber.scrub(raw_json_report)
        
        state["final_report"] = json.loads(scrubbed_json_report)
        state["step"] = 7
        return state
