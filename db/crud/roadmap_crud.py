from sqlalchemy.orm import Session
from db.models.roadmap import RoadMap

def save_roadmap(db: Session, user_id: str, goal_id: str, roadmap_data: dict):
    existing = db.query(RoadMap).filter_by(goal_id=goal_id).first()
    if existing:
        existing.structured_roadmaps = roadmap_data
    else:
        db_roadmap = RoadMap(user_id=user_id, goal_id=goal_id, structured_roadmaps=roadmap_data)
        db.add(db_roadmap )
    db.commit()

def get_roadmap(db: Session, user_id: str, goal_id: str):
    return db.query(RoadMap).filter_by(user_id=user_id, goal_id=goal_id).first()