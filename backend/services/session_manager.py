from google.adk.sessions import DatabaseSessionService
from typing import Optional
import time
import psycopg2
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
load_dotenv()
db_url = os.getenv("ADK_DB_URL")

def wait_for_db(url: str, timeout: int = 30):
    parsed = urlparse(url)
    user = parsed.username
    password = parsed.password
    host = parsed.hostname
    port = parsed.port
    dbname = parsed.path.lstrip('/')

    start = time.time()
    while time.time() - start < timeout:
        try:
            conn = psycopg2.connect(
                dbname=dbname, user=user, password=password,
                host=host, port=port
            )
            conn.close()
            print("✅ ADK DB is ready.")
            return
        except psycopg2.OperationalError:
            print("⏳ Waiting for ADK DB to be ready...")
            time.sleep(1)
    raise Exception("❌ Timed out waiting for ADK DB.")

# Call this before initializing the service
wait_for_db(db_url)

session_service = DatabaseSessionService(db_url=db_url)
def get_or_create_session(app_name: str, user_id: str, initial_state: dict) -> str:
    existing_sessions = session_service.list_sessions(app_name=app_name, user_id=user_id)
    if existing_sessions.sessions:
        return existing_sessions.sessions[0].id  # reuse latest
    new_session = session_service.create_session(app_name=app_name, user_id=user_id, state=initial_state)
    return new_session.id
