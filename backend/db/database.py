from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import time
from dotenv import load_dotenv

load_dotenv()

def wait_for_db_socket(socket_path: str, timeout: int = 30):
    print(f"⏳ Waiting for DB socket: {socket_path}")
    start = time.time()
    while time.time() - start < timeout:
        if os.path.exists(socket_path):
            print("✅ Unix socket ready.")
            return
        time.sleep(1)
    raise Exception("❌ Timed out waiting for DB socket.")

def init_db_engine():
    socket_path = f"/cloudsql/{os.getenv('INSTANCE_CONNECTION_NAME')}/.s.PGSQL.5432"
    wait_for_db_socket(socket_path)

    db_url = sqlalchemy.engine.URL.create(
        drivername="postgresql+pg8000",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("APP_DB_NAME"),
        query={"unix_sock": socket_path}
    )


    return create_engine(db_url)

engine = init_db_engine()

# Test connection
with engine.connect() as conn:
    print("✅ Connected successfully!")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
