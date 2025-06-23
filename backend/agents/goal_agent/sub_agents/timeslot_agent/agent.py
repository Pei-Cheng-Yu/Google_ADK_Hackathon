from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from typing import Annotated
from typing import List, Literal, Optional
from google.adk.tools.tool_context import ToolContext
from datetime import datetime
from .prompts import get_timeslot_agent_prompt
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
def store_available_slot(available_slots: dict, tool_context: ToolContext) -> dict:
    """store_available_slots

    Args:
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
    
        tool_context (ToolContext): Context for accessing and updating session state
   
    Returns:
        dict: the available_slots
    """
    tool_context.state["available_slots"] = available_slots
    return {"message": f"available_slots '{available_slots}' stored."}

    
timeslot_agent = LlmAgent(
    name = "timeslot_agent",
    model = "gemini-2.0-flash",
    instruction = get_timeslot_agent_prompt(),
    tools=[get_available_slots, store_available_slot]
)