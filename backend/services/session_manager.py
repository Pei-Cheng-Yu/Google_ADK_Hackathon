from google.adk.sessions import DatabaseSessionService
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import time
import socket

load_dotenv()

INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME")
ADK_DB_NAME = os.getenv("ADK_DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# Construct SQLAlchemy URL with Unix socket
db_url = URL.create(
    drivername="postgresql+pg8000",
    username=DB_USER,
    password=DB_PASS,
    database=ADK_DB_NAME,
    query={"unix_sock": f"/cloudsql/{INSTANCE_CONNECTION_NAME}/.s.PGSQL.5432"}
)

# Wait for socket to appear
def wait_for_db_socket(socket_path: str, timeout: int = 30):
    print(f"⏳ Waiting for DB socket: {socket_path}")
    start = time.time()
    while time.time() - start < timeout:
        if os.path.exists(socket_path):
            print("✅ Unix socket ready.")
            return
        time.sleep(1)
    raise Exception("❌ Timed out waiting for ADK DB socket.")

wait_for_db_socket(f"/cloudsql/{INSTANCE_CONNECTION_NAME}/.s.PGSQL.5432")

# Init ADK session service
session_service = DatabaseSessionService(db_url=str(db_url))

def get_or_create_session(app_name: str, user_id: str, initial_state: dict) -> str:
    existing_sessions = session_service.list_sessions(app_name=app_name, user_id=user_id)
    if existing_sessions.sessions:
        return existing_sessions.sessions[0].id
    new_session = session_service.create_session(app_name=app_name, user_id=user_id, state=initial_state)
    return new_session.id
