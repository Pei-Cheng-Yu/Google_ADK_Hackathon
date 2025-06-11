from google.adk.runners import Runner
from agents.goal_agent import agent
from services.session_manager import session_service, get_or_create_session
from utils.utils import call_agent_async  # already handles async run
from tools import availability_tools
APP_NAME = "Memory Agent"
from google.adk.tools import ToolContext
async def run_memory_agent(user_id: str, user_input: str) -> dict:
    # Step 1: Get or create session
    session_id = get_or_create_session(
        app_name=APP_NAME,
        user_id=user_id,
        initial_state={"user_name": user_id, "reminders": []},
    )
    
    # Step 2: Setup runner
    runner = Runner(
        agent=agent.root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
   
    # Step 3: Call agent
    result = await call_agent_async(runner, user_id, session_id, user_input)
    return result


