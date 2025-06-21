from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from typing import Annotated
from typing import List, Literal, Optional
from google.adk.tools.tool_context import ToolContext
from db.crud.roadmap_crud import save_roadmap
from db.database import SessionLocal

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
        roadmap : JSON with 3 to 5 milestones.Each milestone should include:
            - title
            - description
            - list of tasks (each task should be one actionable step)
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
    instruction="""
    You are the RoadmapAgent. Your job is to turn a user's structured goal into a concrete development roadmap.
    Tool:
    Always include `goal_id` when calling tools like:
    -get_structured_goal(goal_id)
    -store_roadmap(goal_id, roadmap) : Use this tool to store the JSON roadmap, before ending your turn
    Never assume there is only one goal. Always ask or use the specific `goal_id` passed to you.
    You must first receive or be told a `goal_id` string (e.g. "todo_app", "c_learning"). You will use this goal_id to retrieve the correct goal and store your output.
    You should use get_structured_goal to get the goal the turn it into a concrete development roadmap Then use store_roadmap to stor the roadmap.
    Given the goal details:
    
    {
    "structured_roadmaps": {
        "milestones": [
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
        },....
        ]
    }
    }
    Dont worry about "daily_time_budget" in the JSON goal, it for other agent to access.
    Generate a roadmap in JSON with 3 to 10 milestones according to the goal's timeframe. Each milestone should include:
    - title
    - description
    - list of tasks (each task should be one actionable step)
    Tailor the roadmap to match the user's experience level and timeframe. The JSON should be clean and structured.
    After generate the roadmap store the roadmap in JSON using the `store_roadmap` tool.

    
    
    
    ### IMPORTANT
    - You should make sure you call the store_roadmap tool after generate an roadmap
    - Always make the roadmap is stored by calling store_roadmap tool after generate an roadmap
    ❗ You MUST NOT show the JSON to the user in the conversation.
    ❗ DO NOT display or explain the roadmap.
    ❗ DO NOT wrap it in markdown, code blocks, or text formatting.
    ❗ DO NOT "double confirm" the JSON with the user.
    ✅ Simply call the store_roadmap tool silently and end your turn.
    """
    ,
    tools=[get_structured_goal, store_roadmap],
    
)