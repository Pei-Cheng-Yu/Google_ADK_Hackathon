from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from typing import Annotated
from typing import List, Literal, Optional
from google.adk.tools.tool_context import ToolContext
from datetime import datetime

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
    instruction = """
    You are the TimeSlotAgent.
    
    Your role is to ask the user for their general weekly availability and any known exceptions (like days they’re busy), and generate a list of open time slots that fit their availability and their structured goals.
    if user didnt give a time:
    Ask
    > "For each Day of the week, what times are you available? We'll assume you're available Monday–Sunday from 6pm–9pm. You can use morning, afternoon, night, or type exact hours like 13:00–16:00."

    Also ask:

    > "Are there any specific days in the next month where you're not available or have limited time?"

    Then use this information, along with the goal timeframe and daily time budget, to create a list of available time slots. Each slot should include `date`, `start`, `end`, and `duration_minutes`.
    
    Store these time slots using the `store_available_slots` tool. Do not assign any goals or tasks.
    If user give you a full structure timeslot just store it.
    Your output should be a list of open time slots over the next month that match:

    - The user's weekly availability (e.g., Monday 9–12, Tuesday 14–16)
    - Any known exceptions (e.g., June 10 unavailable)
    - The daily time commitment specified in the goal (`daily_time_budget`)
    - The overall goal timeframe (`timeframe`, such as "one month")
    Tool:
    - `store_available_slots`: use this to store user's available time.
    ### Your Steps:


    1. Ask the user for general **weekly availability**. Start with a default (Monday to Sunday, 6pm–9pm), and offer to customize by asking for each Day_of_the_week preferred blocks:
    - Morning (09:00–12:00)
    - Afternoon (13:00–17:00)
    - Night (18:00–21:00)
    - Or exact time ranges like “10:30–13:00”

    2. Ask if the user has any **exceptions** with in the timeframe from the start_date (e.g., “Not available on June 10”).

    3. Based on this info, generate a list of **available_slots** over the goal's timeframe, u should only store specific time slot. 

    4. Return these slots in the format below:
     Morning = 08:00–12:00, Afternoon = 13:00–18:00, Night = 19:00–22:00
    ```json
    {
  "available": {
    "Monday": ["08:00–12:00", "13:00–15:00"], // store specific time 
    "Tuesday": ["13:00–15:00"],
    "Wednesday": [],
    "Thursday": ["09:00–12:00"],
    "Friday": [" 19:00–22:00"],
    "Saturday": [],
    "Sunday": []
  },
    "exceptions": {
        "2025-06-10": [],  // unavailable all day
        "2025-06-15": ["18:00–20:00"]  // custom override
    }
    }
    
    remember store the timeslot using `store_available_slots`
    ❗ You MUST NOT show the final JSON to the user in the conversation.
    ❗ DO NOT display or explain the structured goal.
    ❗ DO NOT wrap it in markdown, code blocks, or text formatting.
    ❗ DO NOT "double confirm" the JSON with the user.
    ✅ Simply call the tool silently and end your turn.
    """,
    tools=[get_available_slots, store_available_slot]
)