from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from typing import Annotated
from typing import List, Literal, Optional
from google.adk.tools.tool_context import ToolContext
from datetime import datetime
from db.crud.plan_crud import store_plan
from db.database import SessionLocal
import json
from .prompts import get_planner_agent_prompt

def get_all_skillpaths(tool_context: ToolContext) -> dict:
    """_summary_

    Args:
        
        tool_context (ToolContext): Context for accessing and updating session state

    Returns:
        dict: all_skillpaths
    """
    goals = tool_context.state.get("goals", {})
    return {
        "skillpaths": [
            {"goal_id": goal_id, "skillpath": data.get("skillpath", {})}
            for goal_id, data in goals.items()
            if "skillpath" in data
        ]
    }
        
def get_daily_plan(tool_context: ToolContext) -> dict:
    """
    Returns the current daily plan from session state, or an empty list if none is stored.
    """
    daily_plan = tool_context.state.get("daily_plan", [])
    return {
        "daily_plan": daily_plan
    }
def get_available_slots(tool_context: ToolContext) -> dict:
    """_summary_

    Args:
        
        tool_context (ToolContext): Context for accessing and updating session state

    Returns:
        dict: the available_slots
    """
    available_slots = tool_context.state.get("available_slots",{})
    return {
        "available_slots": available_slots
    }
    
def store_daily_plan(daily_plan: dict, tool_context) -> dict:
    """_summary_

    Args:
        ```json
   {
    "daily_plan": [
        {
        "date": "2025-06-02",
        "items": [
            {
            "type": "task",
            "description": "string",
            "tags": ["string", ...],
            "resource": ["youtube_video_title", "example_platform", "example_app", "python_docs",...]
            "title": "Set up project repo",
            "Day_of_the_week": "Monday",
            "start_time": "13:00",
            "end_time": "14:00",
            "duration_min": 60,
            "milestone": "1",
            "goal_id": "`goal_id"
            }
        ]
        }
    ]
    }
        tool_context (ToolContext): Context for accessing and updating session state

    Returns:
        dict: the available_slots
    """
    tool_context.state["daily_plan"] = daily_plan
    user_id = tool_context._invocation_context.user_id
    db = SessionLocal()
    
    try:
        store_plan(db=db, user_id=user_id, daily_plan=daily_plan["daily_plan"])
    finally:
        db.close()
    return {"message": f"daily_plan '{daily_plan}' stored."}


def get_current_date() -> dict:
    """
       Get the current date 
    """
    return {
        "current_date":  datetime.today().date().isoformat()
    }



planner_agent = LlmAgent(
    name="planner_agent",
    model="gemini-2.0-flash",
    instruction=get_planner_agent_prompt(),
    tools = [
    get_all_skillpaths,
    get_available_slots,
    store_daily_plan,
   
    ]
)