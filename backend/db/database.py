from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
load_dotenv()


def init_db_engine():
    return create_engine(
        URL.create(
            drivername="postgresql+pg8000",
            username=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("APP_DB_NAME"),
            query={
                "unix_sock": f"/cloudsql/{os.getenv('INSTANCE_CONNECTION_NAME')}/.s.PGSQL.5432"
            }
        )
    )
    
    
engine = init_db_engine()
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