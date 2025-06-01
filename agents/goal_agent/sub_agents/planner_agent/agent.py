from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from typing import Annotated
from typing import List, Literal, Optional
from google.adk.tools.tool_context import ToolContext

def get_all_structured_goals(tool_context: ToolContext) -> dict:
    """_summary_

    Args:
        
        tool_context (ToolContext): Context for accessing and updating session state

    Returns:
        dict: all_structured_goals
    """
    goals = tool_context.state.get("goals", {})
    return {
        "goals": [
            {"goal_id": goal_id, "structured_goal": data.get("structured_goal", {})}
            for goal_id, data in goals.items()
        ]
    }

def get_all_roadmaps(tool_context: ToolContext) -> dict:
    """_summary_

    Args:
        
        tool_context (ToolContext): Context for accessing and updating session state

    Returns:
        dict: all_roadmaps
    """
    goals = tool_context.state.get("goals", {})
    return {
        "roadmaps": [
            {"goal_id": goal_id, "roadmap": data.get("roadmap", {})}
            for goal_id, data in goals.items()
            if "roadmap" in data
        ]
    }

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
    
def store_daily_plan(daily_plan: dict, tool_context: ToolContext) -> dict:
    """_summary_

    Args:
        "daily_plan": [
        {
        "date": "2025-06-02",
        "items": [
            {
            "type": "task",
            "title": "Set up project repo",
            "Day_of_the_week": "Tuesday",
            "start_time": "13:00",
            "end_time": "14:00",
            "duration_min": 60,
            "milestone": "Setup",
            "goal_id": "abc123"
            },
            ...
        ]
        }
        ]
        tool_context (ToolContext): Context for accessing and updating session state

    Returns:
        dict: the available_slots
    """
    tool_context.state["daily_plan"] = daily_plan
    return {"message": f"daily_plan '{daily_plan}' stored."}

def store_per_goal_plan(per_goal_plan: dict, tool_context: ToolContext) -> dict:
    """_summary_

    Args:
        "per_goal_plan": [
        {
        "goal_id": "abc123",
        "plan": [
            {
            "date": "2025-06-02",
            "Day_of_the_week": "Tuesday",
            "start_time": "13:00",
            "end_time": "14:00",
            "type": "task",
            "title": "Set up project repo",
            "duration_min": 60,
            "milestone": "Setup"
            },
            ...
        ]
        }
    ]
        tool_context (ToolContext): Context for accessing and updating session state

    Returns:
        dict: the available_slots
    """
    tool_context.state["per_goal_plan"] = per_goal_plan
    return {"message": f"per_goal_plan '{per_goal_plan}' stored."}

def store_unsigned_plan(unsigned_plan: dict , tool_context: ToolContext) -> dict:
    """_summary_

    Args:
          
        "unassigned": [
        {
        "type": "task",
        "title": "Write unit tests",
        "duration_min": 90,
        "milestone": "Testing",
        "goal_id": "abc123",
        "reason": "Not enough available time"
        }
        ]
        
        tool_context (ToolContext): Context for accessing and updating session state

    Returns:
        dict: the unsigned_plan
    """
    tool_context.state["unsigned_plan"] = unsigned_plan
    return {"message": f"unsigned_plan '{unsigned_plan}' stored."}

def store_remain_slots(remain_slots: dict , tool_context: ToolContext) -> dict:
    """_summary_

    Args:
          
        "remain_slots": [
            {
            "Day_of_the_week": "Tuesday",
            "date": "2025-06-03",
            "start": "09:00",
            "end": "12:00",
            "duration_minutes": 180
            },
            ...
        ]
        
        tool_context (ToolContext): Context for accessing and updating session state

    Returns:
        dict: the remain_slot
    """
    tool_context.state["remain_slots"] = remain_slots
    return {"message": f"remain_slots '{remain_slots}' stored."}

planner_agent = LlmAgent(
    name="planner_agent",
    model="gemini-2.0-flash",
    instruction="""
    You are PlannerAgent. Your job is to create a complete time-based plan for all current goals. You will retrieve goals, tasks, learning steps, and available time blocks using the appropriate tools. Then you will generate two versions of the schedule and store them using provided tools.

    ---

    🔧 TOOLS TO USE

    Fetch:
    - Call `get_all_structured_goals` to retrieve all structured goals (each with a unique `goal_id`).
    - Call `get_all_roadmaps` to get tasks and milestones for each goal.
    - Call `get_all_skillpaths` to get learning steps for each goal.
    - Call `get_available_slots` to get time blocks with:
    - `date`, `Day_of_the_week`, `start`, `end`, and `duration_minutes`.

    Store:
    - Call `store_daily_plan` to store the `daily_plan` (grouped by date).

    ---

    🧠 YOUR TASK

    Step 1: Collect all goals, roadmaps, skillpaths, and time slots.  
    Step 2: Assign tasks and learning items from `learning_path` of the skillpaths into the available slots. Follow these rules:
    - Respect the `duration_min` of each item.
    - Assign a precise `start_time` and `end_time` based on the slot.
    - Avoid overlapping items.
    - Prioritize filling earlier dates first.
    - Balance work between multiple goals and types.
    - Don't exceed the `daily_time_budget` for each goal
    - Generate a version fit in `daily_plan` format

    📦 OUTPUT FORMAT

    1. `daily_plan` (grouped by date):

    ```json
    {
    "daily_plan": [
        {
        "date": "2025-06-02",
        "items": [
            {
            "type": "task",
            "title": "Set up project repo",
            "Day_of_the_week": "Tuesday",
            "start_time": "13:00",
            "end_time": "14:00",
            "duration_min": 60,
            "milestone": "Setup",
            "goal_id": "abc123"
            },
            ...
        ]
        "unassigned": [
        {
        "type": "task",
        "title": "Write unit tests",
        "duration_min": 90,
        "milestone": "Testing",
        "goal_id": "abc123",
        "reason": "Not enough available time"
        }
        }
    
    ]
    }
    
    
    
    - You should make sure you call the storing tool after generate an plan
    - Always make the plan is stored by calling storing tools after generate an plan
    ❗ You MUST NOT show the final JSON to the user in the conversation.
    ❗ DO NOT display or explain the structured goal.
    ❗ DO NOT wrap it in markdown, code blocks, or text formatting.
    ❗ DO NOT "double confirm" the JSON with the user.
    ✅ Simply call the tool silently and end your turn.
    If something fail, feel free to tell user
    """,
    tools = [
    get_all_roadmaps,
    get_all_skillpaths,
    get_all_structured_goals,
    get_available_slots,
    store_daily_plan,

    ]
)