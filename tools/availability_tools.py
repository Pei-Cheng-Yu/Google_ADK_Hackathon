# tools/availability_tools.py

from google.adk.tools.tool_context import ToolContext

def get_available_slots(tool_context: ToolContext) -> dict:
    return {
        "available_slots": tool_context.state.get("available_slots", {})
    }
def get_skillpath(goal_id: str, tool_context: ToolContext) -> dict:
    result = {}
    goals = tool_context.state.get("goals", {})
    if goal_id not in goals:
        result = {}
    result= goals[goal_id]["roadmap"] 
    return result
