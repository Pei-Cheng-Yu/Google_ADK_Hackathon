from google.genai import types
import json

async def call_agent_async(runner, user_id, session_id, user_input):
    content = types.Content(role="user", parts=[types.Part(text=user_input)])
    final_response_text = None
    
    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            # Process each event and get the final response if available
            response = await process_agent_response(event)
            if response:
                final_response_text = response
    except Exception as e:
        print(f"Error during agent call: {e}")
    return final_response_text
        
async def process_agent_response(event):
      # Handle tool/function call parts
    if hasattr(event, "function_call") and event.function_call:
        print("⚙️ Function call detected:", event.function_call.name)
        print("🔧 Args:", event.function_call.args)

        # Return args (can be dict or JSON string depending on ADK version)
        try:
            if isinstance(event.function_call.args, str):
                return json.loads(event.function_call.args)
            return event.function_call.args
        except Exception as e:
            print(f"❌ Error parsing function_call args: {e}")
            return None

    # Handle standard final responses
    if event.is_final_response():
        if (
            event.content
            and event.content.parts
            and hasattr(event.content.parts[0], "text")
            and event.content.parts[0].text
        ):
            return event.content.parts[0].text.strip()
