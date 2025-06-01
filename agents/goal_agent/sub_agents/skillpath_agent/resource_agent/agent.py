from google.adk.agents import Agent
from google.adk.tools import google_search

resource_agent = Agent(
    name="resource_agent",
    model="gemini-2.0-flash",
    instruction="Help the user find the best tutorials or guides.",
    tools=[google_search],
)
