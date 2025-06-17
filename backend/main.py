from fastapi import FastAPI
from api.routes import router as api_router
from auth.routes import router as auth_router
from dotenv import load_dotenv
import os
from db.database import init_db
from fastapi.middleware.cors import CORSMiddleware


load_dotenv(override=True)
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
print("Allowed origins:", allowed_origins)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(api_router)


init_db()
