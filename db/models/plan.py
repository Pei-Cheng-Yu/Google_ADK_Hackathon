from sqlalchemy import Column, Integer, String, Date, Time, JSON, ForeignKey
from db.database import Base
from datetime import datetime

class DailyPlanItem(Base):
    __tablename__ = "daily_plan_items"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    goal_id = Column(String, index=True)
    date = Column(Date, index=True)
    title = Column(String)
    description = Column(String, nullable=True)
    tags = Column(JSON, nullable=True)
    resource = Column(JSON, nullable=True)
    milestone = Column(String, nullable=True)
    type = Column(String) 
    start_time = Column(Time)
    end_time = Column(Time)
    duration_min = Column(Integer)
    day_of_the_week = Column(String) 
    raw = Column(JSON, nullable=True)  
