import os
import json
import uuid
from typing import Dict, Any
from agents_cli.security import LocalEncryptor

SESSIONS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sessions")

class SessionManager:
    def __init__(self, password: str = "default-education-agent-secure-key"):
        self.encryptor = LocalEncryptor(password)
        os.makedirs(SESSIONS_DIR, exist_ok=True)

    def _get_filepath(self, session_id: str) -> str:
        return os.path.join(SESSIONS_DIR, f"{session_id}.enc")

    def create_session(self) -> str:
        """Create a new session ID and save an empty state."""
        session_id = str(uuid.uuid4())
        initial_state = {
            "session_id": session_id,
            "step": 0,
            "subject": "",
            "level": "",
            "target": "",
            "milestones": "",
            "student_name": "",
            "student_email": "",
            "curriculum_title": "",
            "curriculum_standards": [],
            "diagnostic_questions": [],
            "diagnostic_answers": {},
            "diagnostic_score": "",
            "weak_topics": [],
            "study_plan": [],
            "quiz_questions": [],
            "quiz_answers": {},
            "quiz_score": "",
            "feedback": [],
            "mastery_level": "",
            "final_report": {}
        }
        self.save_session(session_id, initial_state)
        return session_id

    def load_session(self, session_id: str) -> Dict[str, Any]:
        """Loads and decrypts the session state."""
        filepath = self._get_filepath(session_id)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Session {session_id} not found.")

        with open(filepath, "r", encoding="utf-8") as f:
            encrypted_data = f.read()

        decrypted_json = self.encryptor.decrypt(encrypted_data)
        return json.loads(decrypted_json)

    def save_session(self, session_id: str, state: Dict[str, Any]) -> None:
        """Encrypts and saves the session state."""
        filepath = self._get_filepath(session_id)
        raw_json = json.dumps(state, indent=2)
        encrypted_data = self.encryptor.encrypt(raw_json)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(encrypted_data)

    def list_sessions(self) -> list:
        """List all available session IDs."""
        if not os.path.exists(SESSIONS_DIR):
            return []
        files = os.listdir(SESSIONS_DIR)
        return [f.replace(".enc", "") for f in files if f.endswith(".enc")]
