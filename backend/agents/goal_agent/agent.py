from google.adk.agents import LlmAgent, SequentialAgent
from .prompts import get_goal_agent_prompt
from pydantic import BaseModel, Field
from typing import Annotated
from typing import List, Literal, Optional
from google.adk.tools.tool_context import ToolContext
from .sub_agents.roadmap_agent.agent import roadmap_agent
from .sub_agents.skillpath_agent.agent import skillpath_agent
from .sub_agents.timeslot_agent.agent import timeslot_agent
from datetime import datetime
from .sub_agents.planner_agent.agent import planner_agent
from db.crud.goal_crud import save_goal
from db.database import SessionLocal

class GoalAgentOutput(BaseModel):
    goal: str = Field(description="Natural language goal provided by the user")
    category: str = Field(description="The topic or domain of the goal")
    timeframe: Optional[str] = Field(default="Not specified", description="Deadline or duration for the goal")
    intent: Literal["Project", "Learning", "Habit"] = Field(description="The type of goal")
    experience_level: Literal["Beginner", "Intermediate", "Advanced"] = Field(description="User's level of experience")
    platform: Optional[Literal["Web", "Mobile", "Offline", "Hybrid"]] = Field(default=None, description="Platform focus for the goal")
    tech_stack: Optional[List[str]] = Field(default=[], description="List of technologies, languages, or tools used")
    features: Optional[List[str]] = Field(default=[], description="Desired capabilities, skills, or features")
    context: Optional[List[str]] = Field(default=[], description="Reason or use case behind the goal")
    daily_time_budget: str = Field(default="Not specified", description="How much time the user can commit daily")
def store_structured_goal(goal_id: str, goal: dict, tool_context: ToolContext) -> dict:
    """store A structured JSON goal object with the following fields:

```json
         {
            "goal": "string",
            "category": "string",
            "timeframe": "string",
            "intent": "Project" | "Learning" | "Habit",
            "experience_level": "Beginner" | "Intermediate" | "Advanced",
            "platform": "Web" | "Mobile" | "Offline" | "Hybrid",
            "tech_stack": [string],
            "features": [string],
            "context": [string],
            "daily_time_budget": "string"
            "start_date": "string"
            }

    Args:
        goal (dict): {
                    "goal": "string",
                    "category": "string",
                    "timeframe": "string",
                    "intent": "Project" | "Learning" | "Habit",
                    "experience_level": "Beginner" | "Intermediate" | "Advanced",
                    "platform": "Web" | "Mobile" | "Offline" | "Hybrid",
                    "tech_stack": [string],
                    "features": [string],
                    "context": [string],
                    "daily_time_budget": "string"
                    "start_date": "string"
                    }
        tool_context (ToolContext): Context for accessing and updating session state

    Returns:
        A confirmation message
    """
    goals = tool_context.state.get("goals", {})
    if goal_id not in goals:
        goals[goal_id] = {}
    goals[goal_id]["structured_goal"] = goal
    tool_context.state["goals"] = goals
    user_id = tool_context._invocation_context.user_id
    db = SessionLocal()
    try:
        save_goal(db, user_id=user_id, goal_id=goal_id, goal_data=goal)
    finally:
        db.close()
    return {"message": f"Structured goal '{goal_id}' stored."}
def get_available_slots(tool_context: ToolContext) -> dict:
    """_summary_

    Args:
        
        tool_context (ToolContext): Context for accessing and updating session state

    Returns:
        dict: the available_slots
    """
    available_slots = tool_context.state.get("available_slots")
    return {
        "available_slots": available_slots
    }
    

def get_current_date() -> dict:
    """
       Get the current date 
    """
    return {
        "current_date":  datetime.today().date().isoformat()
    }

def list_goal_ids(tool_context: ToolContext) -> dict:
    goals = tool_context.state.get("goals", {})
    return {"goal_ids": list(goals.keys())}

def get_goal_by_id(goal_id: str, tool_context: ToolContext) -> dict:
    goals = tool_context.state.get("goals", {})
    goal = goals.get(goal_id, {})
    if goal:
        return {"goal_id": goal_id, "goal": goal}
    return {"error": "Goal not found"}

def get_available_slots(tool_context: ToolContext) -> dict:
    """Returns all stored skillpaths"""
    available_slots = tool_context.state.get("available_slots")
    return {
        "available_slots": available_slots
    }
def get_skillpath(goal_id: str, tool_context: ToolContext) -> dict:
    """
    Retrieve the skillpath for a specific goal.

    Args:
        goal_id (str): The ID of the goal to fetch the skillpath for.
        tool_context (ToolContext): The ADK tool context holding session state.

    Returns:
        dict: A dictionary containing the goal_id and associated skillpath,
              or an empty dict if not found.
    """
    goals = tool_context.state.get("goals", {})
    skillpath = goals.get(goal_id, {}).get("skillpath", {})

    return {
        "goal_id": goal_id,
        "skillpath": skillpath
    }
    
def get_daily_plan( tool_context: ToolContext) -> dict:
    """_summary_

        tool_context (ToolContext): Context for accessing and updating session state

    Returns:
        dict: the available_slots
    """
    daily_plan=tool_context.state.get(" daily_plan", {})
    return {
        
       "daily_plan": daily_plan
    }
S_agent = SequentialAgent(
    name="S_agent",
    sub_agents=[roadmap_agent,skillpath_agent],
    description="A S_agent run the roadmap and skillpath agent",
)

root_agent = LlmAgent(
    name ="goal_agent",
    model="gemini-2.0-flash",
    instruction=get_goal_agent_prompt(),
    tools=[get_daily_plan,get_available_slots,store_structured_goal, list_goal_ids, get_goal_by_id, get_current_date, get_available_slots, get_skillpath],
    sub_agents=[S_agent, timeslot_agent, planner_agent],
)