from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from typing import Annotated
from typing import List, Literal, Optional
from google.adk.tools.tool_context import ToolContext
from .resource_agent.agent import resource_agent
from google.adk.tools.agent_tool import AgentTool
from db.crud.skillpath_crud import save_skillpath
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
    instruction="""
    You are a SkillPathAgent in a multi-agent system.

    Your goal is to generate a personalized learning path based on the user's structured goal and roadmap.

    ### TOOL USAGE

    You MUST begin by calling the following tools to retrieve context:
    Always include `goal_id` when calling tools like:
    1. `get_structured_goal(goal_id)` – use this to retrieve the user's structured learning goal.
    2. `get_stored_roadmap(goal_id)` – use this to retrieve the milestone-based roadmap (each with tasks) generated earlier.
    3. `store_skillpath(goal_id, skillpath)` store the skillpath you generate before ending your turn.
    
    Do not generate any learning path until you have retrieved and examined both.
    Always operate within the scope of a single `goal_id`. Do not mix goals.
    ### TASK

    After retrieving both:

    - For **each task** listed in each milestone from the roadmap:
    - Create a corresponding **learning unit** with:
        - `title`: a short name for the skill
        - `description`: a 1–2 sentence summary explaining the learning objective
        - `milestone`: current milestone index from the roadmap
        - `estimated_hours`: an estimated duration (typically 0.5 to 2 hours)
        - `tags`: e.g., "video", "reading", "flashcards", "app", "speaking", "role-play"

    - Organize the learning units in a logical **skill-based order**, NOT by week.

    - Consider `experience_level`, `intent`, and `context` from the structured goal to shape the learning suggestions.

    ### Skillpath FORMAT

    Skillpath must strictly match the following JSON format:

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
     Be concise, and practical.
    
    ### RESOURCE RETRIEVAL

    For each learning unit, try to suggest **1–2 relevant learning resources** in the `resource` field.

    - search for high-quality material.
    - Only include platform, website or youtube video title in real world content.
    - Resources may include tutorials, videos, apps, guides, or exercises.
    - Prefer beginner-friendly and free content when possible.

    If no appropriate resource is found, return an empty list: `"resource": []`
   
    
    ### IMPORTANT
    After generate the skillpath store the skillpath in JSON using the store_skillpath tool.
    Always include `goal_id` when calling tools 
    After storing the skillpath, transfer back to root_agent
    ❗ You MUST NOT show the final JSON to the user in the conversation.
    ❗ DO NOT display or explain the skillpath.
    ❗ DO NOT wrap it in markdown, code blocks, or text formatting.
    ❗ DO NOT "double confirm" the JSON with the user.
    ❗ DO NOT fake up any resource
    ✅ Simply call the store_roadmap tool silently and end your turn.
    
    """
    ,
    tools=[get_stored_roadmap, get_structured_goal,store_skillpath]
)