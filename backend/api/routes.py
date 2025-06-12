from services.runner_service import run_memory_agent
from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from db.database import get_db
from sqlalchemy.orm import Session
from db.crud.goal_crud import get_all_goal, get_goal_by_id
from db.crud.roadmap_crud import get_roadmap
from db.crud.skillpath_crud import get_skillpath
from db.crud.plan_crud import get_plan
from db.models.user import User
from auth.protected import get_current_user

router = APIRouter()

class AgentRequest(BaseModel):
    user_input: str
    
@router.post("/run_memory_agent")
async def run_agent(request: AgentRequest,current_user: User = Depends(get_current_user)):
    result = await run_memory_agent(str(current_user.id),request.user_input)
    return {"response": result}

@router.get("/goal")
def get_all_goals(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_all_goal(db, str(current_user.id))  

@router.get("/goal/{goal_id}")
def get_goal(goal_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_goal_by_id(db, str(current_user.id), goal_id)

@router.get("/roadmap/{goal_id}")
def get_roadmap_route(goal_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_roadmap(db, user_id=str(current_user.id), goal_id=goal_id)

@router.get("/skillpath/{goal_id}")
def get_skillpath_route(goal_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_skillpath(db, user_id=str(current_user.id), goal_id=goal_id)

@router.get("/plan")
def get_plan_route(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_plan(db, user_id=str(current_user.id))

@router.get("/protected")
def read_protected(current_user: User = Depends(get_current_user)):
    return {"user": current_user.username}


