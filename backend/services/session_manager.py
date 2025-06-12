from google.adk.sessions import DatabaseSessionService
from typing import Optional

db_url = "sqlite:///./my_agent_data2.db"
session_service = DatabaseSessionService(db_url=db_url)

def get_or_create_session(app_name: str, user_id: str, initial_state: dict) -> str:
    existing_sessions = session_service.list_sessions(app_name=app_name, user_id=user_id)
    if existing_sessions.sessions:
        return existing_sessions.sessions[0].id  # reuse latest
    new_session = session_service.create_session(app_name=app_name, user_id=user_id, state=initial_state)
    return new_session.id
