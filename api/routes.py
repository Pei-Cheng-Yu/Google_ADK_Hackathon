from services.runner_service import run_memory_agent
from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from db.database import get_db
from sqlalchemy.orm import Session
from db.crud.goal_crud import get_all_goal, get_goal_by_id
from db.crud.roadmap_crud import get_roadmap
from db.crud.skillpath_crud import get_skillpath
from db.crud.plan_crud import get_plan

router = APIRouter()

class AgentRequest(BaseModel):
    user_id: str
    user_input: str
    
@router.post("/run_memory_agent")
async def run_agent(request: AgentRequest):
    result = await run_memory_agent(request.user_id,request.user_input)
    return {"response": result}

@router.get("/goal")
def get_all_goals(user_id: str, db: Session = Depends(get_db)):
    return get_all_goal(db, user_id)

@router.get("/goal/{goal_id}")
def get_goal(goal_id: str, user_id: str, db: Session = Depends(get_db)):
    return get_goal_by_id(db, user_id, goal_id)

@router.get("/roadmap/{goal_id}")
def get_roadmap_route(db: Session = Depends(get_db), user_id: str = ..., goal_id: str = ...):
    return get_roadmap(db, user_id=user_id, goal_id=goal_id)

@router.get("/skillpath/{goal_id}")
def get_skillpath_route(db: Session = Depends(get_db), user_id: str = ..., goal_id: str = ...):
    return get_skillpath(db, user_id=user_id, goal_id=goal_id)

@router.get("/plan")
def get_plan_route(db: Session = Depends(get_db), user_id: str = ...):
    return get_plan(db, user_id= user_id)