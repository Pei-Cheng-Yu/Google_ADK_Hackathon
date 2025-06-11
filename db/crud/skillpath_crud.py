from sqlalchemy.orm import Session
from db.models.skillpath import SkillPath

def save_skillpath(db: Session, user_id: str, goal_id: str, skillpath_data: dict):
    existing = db.query(SkillPath).filter_by(user_id=user_id, goal_id=goal_id).first()
    if existing:
        existing.structured_skillpaths = skillpath_data
    else:
        db_skillpath = SkillPath(user_id=user_id, goal_id=goal_id, structured_skillpaths=skillpath_data)
        db.add(db_skillpath)
    db.commit()
    
def get_skillpath(db: Session, user_id: str, goal_id: str):
    return db.query(SkillPath).filter_by(user_id=user_id, goal_id=goal_id).first()    