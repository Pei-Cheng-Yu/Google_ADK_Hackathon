from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db.models.user import User
from .hash import verify_password, hash_password
from .jwt import create_access_token
from fastapi import Form
from pydantic import BaseModel
router = APIRouter()


class SignupRequest(BaseModel):
    username: str
    password: str
    
    
@router.post("/signup")
def signup(
    data: SignupRequest,
    db: Session = Depends(get_db)):
    username = data.username
    password = data.password
    user = db.query(User).filter_by(username=username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed = hash_password(password)
    new_user = User(username=username, password=hashed)
    db.add(new_user)
    db.commit()
    return {"message": "User created"}

@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    
    user = db.query(User).filter_by(username=username).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}