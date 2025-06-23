from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from typing import Annotated
from typing import List, Literal, Optional
from google.adk.tools.tool_context import ToolContext
from db.crud.roadmap_crud import save_roadmap
from db.database import SessionLocal
from .prompts import get_roadmap_agent_prompt
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


def store_roadmap(goal_id: str, roadmap: dict, tool_context: ToolContext) -> dict:
    """ store a roadmap in JSON with 3 to 10 milestones. Each milestone should include:
        - title
        - description
        - list of tasks (each task should be one actionable step)

        
    
    Args:
        roadmap : JSON with 3 to 10 milestones.
        {
            "milestones": [
                {
                "title": "string",
                "description": "string",
                "tasks": ["string", "string", ...]
                },
                ...
            ]
        }

        tool_context (ToolContext): Context for accessing and updating session state

    Returns:
        dict: the roadmap
    """
    goals = tool_context.state.get("goals", {})
    if goal_id not in goals:
        goals[goal_id] = {}
    goals[goal_id]["roadmap"] = roadmap
    tool_context.state["goals"] = goals
    user_id = tool_context._invocation_context.user_id
    db = SessionLocal()
    try:
        save_roadmap(db, user_id=user_id, goal_id=goal_id, roadmap_data=roadmap)
    finally:
        db.close()
    return {"message": f"Roadmap stored for goal '{goal_id}'."}
    
    
roadmap_agent = LlmAgent(
    name ="roadmap_agent",
    model="gemini-2.0-flash",
    instruction=get_roadmap_agent_prompt(),
    tools=[get_structured_goal, store_roadmap],
    
)