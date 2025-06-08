from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from typing import Annotated
from typing import List, Literal, Optional
from google.adk.tools.tool_context import ToolContext
from datetime import datetime
from db.crud.plan_crud import store_plan
from db.database import SessionLocal
import json
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
    user_id = tool_context.state.get("user_id", "test")
    db = SessionLocal()
    
    try:
        store_plan(db=db, user_id=user_id, daily_plan=daily_plan["daily_plan"])
    finally:
        db.close()
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
def get_date_weekday(date: str) -> dict:
    """
    Get the weekday name of a date string in YYYY-MM-DD format.
    
    Args:
        date (str): A date string like "2025-06-01"
        
    Returns:
        dict: {"weekday": "Sunday"} (or other day name)
    """
    date_obj = datetime.strptime(date, "%Y-%m-%d").date()

    # Correct way to get weekday name
    day_of_week = date_obj.strftime("%A")

    return {
        "weekday": day_of_week
    }


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
    ```json
    {
    "available": 
     {
        "available": {
            "Monday": ["morning", "13:00–15:00", "night"],
            "Tuesday": ["afternoon"],
            "Wednesday": [],
            "Thursday": ["09:00–12:00"],
            "Friday": ["night"],
            "Saturday": [],
            "Sunday": []
        },
        "exceptions": {
            "2025-06-10": [],  
            "2025-06-15": ["18:00–20:00"]  
        }
        }
    Morning = 08:00–12:00, Afternoon = 13:00–18:00, Night = 19:00–22:00
    - Call `get_date_weekday` to get the day of the week of a specific date
    Store:
    - Call `store_daily_plan` to store the `daily_plan` (grouped by date).

    ---

    🧠 YOUR TASK

    Step 1: Collect all goals, roadmaps, skillpaths, and time slots.  
    Step 2. Schedule tasks and learning items using a weekly availability template:

    - Begin planning from the `start_date` found in each goal's `structured_goal`.
    - For each day starting from that date:
    - Use the `available` weekly pattern to determine available blocks (e.g., "Monday": ["morning", "13:00–15:00"]).
    - Skip any date listed in `exceptions` (if fully unavailable) or apply override blocks if specified.
    - Compute the actual available date blocks by combining the weekly template with the calendar.
    - For each available time block:
    - Assign a task or learning item that fits the time block (`estimated_hours` to `duration_min`).
    - Continue this daily scheduling process **week by week**, until all items are scheduled or no valid time remains.
    - Do not exceed `daily_time_budget` per goal.
    - Avoid overlapping assignments and balance task/learning types.

    Once all items are assigned or no more time is available, store the result in `daily_plan`.
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
        }
      ]
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
    get_date_weekday
    ]
)