from sqlalchemy.orm import Session
from db.database import User
from sqlalchemy.orm import Session
from db.models.user import User  # assuming your model is here
from auth.hash import Hash  # bcrypt utility for passwords


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, username: str, password: str):
    hashed_pw = Hash.bcrypt(password)
    db_user = User(username=username, password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not Hash.verify(password, user.password):
        return False
    return user
