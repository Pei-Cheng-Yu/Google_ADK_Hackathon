from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime
from db.database import Base

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    goal_id = Column(String, index=True)
    structured_goals = Column(JSON) 
