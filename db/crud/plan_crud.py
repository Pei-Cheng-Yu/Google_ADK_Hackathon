from datetime import datetime
from db.models.plan import DailyPlanItem

from sqlalchemy.orm import Session

def store_plan(db: Session ,user_id: str, daily_plan: list):
    for day in daily_plan:
        date = datetime.strptime(day["date"], "%Y-%m-%d").date()
        for item in day["items"]:
            db_item = DailyPlanItem(
                user_id=user_id,
                goal_id = item.get("goal_id"),
                date=date,  
                title = item.get("title"),
                type = item.get("type"),
                tags = item.get("tags"),
                description = item.get("description"),
                resource = item.get("resource"),
                milestone = item.get("milestone"),
                start_time=datetime.strptime(item["start_time"], "%H:%M").time(),
                end_time=datetime.strptime(item["end_time"], "%H:%M").time(),
                duration_min=item.get("duration_min"),
                day_of_the_week=item.get("Day_of_the_week"),
                raw=item  # save full original item JSON if you want
            )
            db.add(db_item)
    db.commit()
    db.close()

def get_plan(db:Session, user_id: str):
    return db.query(DailyPlanItem).filter_by(user_id=user_id).all()