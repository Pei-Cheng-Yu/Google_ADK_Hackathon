from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime
from db.database import Base

class SkillPath(Base):
    __tablename__ = "skillpaths"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    goal_id = Column(String, index=True)
    structured_skillpaths = Column(JSON) 
