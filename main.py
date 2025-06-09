from fastapi import FastAPI
from api.routes import router as api_router
from auth.routes import router as auth_router
from dotenv import load_dotenv
import os
from db.database import init_db
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
app = FastAPI()
app.include_router(auth_router)
app.include_router(api_router)
init_db()