from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from typing import Annotated
from typing import List, Literal, Optional
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.agent_tool import AgentTool
from db.crud.skillpath_crud import save_skillpath
from db.database import SessionLocal
from .prompts import get_skillpath_agent_prompt
def get_structured_goal(goal_id: str, tool_context: ToolContext) -> dict:
    """_summary_

    Args:
        
        tool_context (ToolContext): Context for accessing and updating session state

    Returns:
        dict: the structured goal
    """
    goals = tool_context.state.get("goals", {})
    structured_goal = goals.get(goal_id, {}).get("structured_goal", {})
    return {"goal_id": goal_id, "structured_goal": structured_goal}



def get_stored_roadmap(goal_id: str, tool_context: ToolContext) -> dict:
    """_summary_

    Args:
        
        tool_context (ToolContext): Context for accessing and updating session state

    Returns:
        dict: the stored_roadmap
    """
    goals = tool_context.state.get("goals", {})
    roadmap = goals.get(goal_id, {}).get("roadmap", {})
    return {"goal_id": goal_id, "roadmap": roadmap}

def store_skillpath(goal_id: str, skillpath: dict, tool_context: ToolContext) -> dict:
    """ store a skillpath in JSON.
        the skillpath format:
        {
        "skill_goal": "<copied from structured_goal.goal>",
        "timeframe": "<copied from structured_goal.timeframe>",
        "start_date": "<copied from structured_goal.start_date>",
        "learning_path": [
            {
            "title": "string",
            "description": "string",
            "milestone": "int",
            "estimated_hours": float,
            "tags": ["string", ...],
            "resource": ["youtube_video_title", "example_platform", "example_app", "python_docs",...]
            }
        ]
        }

        
    
    Args:
        skillpath : JSON 
        {
        "skill_goal": "<copied from structured_goal.goal>",
        "timeframe": "<copied from structured_goal.timeframe>",
        "start_date": "<copied from structured_goal.start_date>",
        "learning_path": [
            {
            "title": "string",
            "description": "string",
            "milestone": "int",
            "estimated_hours": float,
            "tags": ["string", ...],
            "resource": ["youtube_video_title", "example_platform", "example_app", "python_docs",...]
            }
        ]
        }
        tool_context (ToolContext): Context for accessing and updating session state

    Returns:
        dict: the roadmap
    """
    goals = tool_context.state.get("goals", {})
    if goal_id not in goals:
        goals[goal_id] = {}
    goals[goal_id]["skillpath"] = skillpath
    tool_context.state["goals"] = goals
    user_id = tool_context._invocation_context.user_id
    db = SessionLocal()
    try:
        save_skillpath(db=db, user_id=user_id, goal_id=goal_id, skillpath_data=skillpath)
    finally:
        db.close()
    return {"message": f"Skillpath stored for goal '{goal_id}'."}
    

skillpath_agent = LlmAgent(
    name = "skillpath_agent",
    model="gemini-2.0-flash",
    instruction=get_skillpath_agent_prompt(),
    tools=[get_stored_roadmap, get_structured_goal,store_skillpath]
)