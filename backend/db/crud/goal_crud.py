from sqlalchemy.orm import Session
from db.models.goal import Goal
from db.models.user import User
from auth.protected import get_current_user
from fastapi import Depends
def save_goal(db: Session,user_id: str ,goal_id: str, goal_data: dict):
    existing = db.query(Goal).filter_by(goal_id=goal_id,user_id=user_id).first()
    if existing:
        existing.structured_goals = goal_data
    else:
        db_goal = Goal(user_id=user_id, goal_id=goal_id, structured_goals=goal_data)
        db.add(db_goal)
    db.commit()

def get_all_goal(db: Session, user_id: str):
    return db.query(Goal).filter_by(user_id=user_id).all()

def get_goal_by_id(db: Session, user_id: str, goal_id: str):
    return db.query(Goal).filter_by(user_id=user_id, goal_id=goal_id).first()