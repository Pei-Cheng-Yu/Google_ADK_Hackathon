from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import JWTError
from db.models.user import User
from db.database import get_db
from sqlalchemy.orm import Session
from auth.jwt import decode_access_token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401)
    except JWTError:
        raise HTTPException(status_code=401)
    user = db.query(User).filter_by(username=username).first()
    if user is None:
        raise HTTPException(status_code=404)
    return user
