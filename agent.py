from tools import search_geography
from openai import OpenAI
import json, os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent / ".env")

client = OpenAI(
    base_url = "https://openrouter.ai/api/v1",
    api_key = os.getenv("OPENROUTER_API_KEY")
)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_geography",
            "description": "tells about the indian geography, himalyas, hills, mountains",
            "parameters":{
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "any question about the geography of india",
                    }
                },
                "required": ["query"]

            }
        }
    }
]
    
conversation_history = [{
    "role": "system",
    "content": (
        "You are a helpful assistant. You have access to these tools \n"
        "1. search_geography- This tool helps to answer the queries baout the geography of india \n"
        "Always use apprpriate tool when answering.\n"
        "Never assume or guess on your own"
    )
}] 

def run_tool(name, args):
        args_dict = json.loads(args)
        if name == "search_geography":
            return search_geography(args_dict['query'])

def run_agent(user_question: str)-> str:

    conversation_history.append({
        "role": "user",
        "content": user_question
    }
    )
    while True:

        response = client.chat.completions.create(
            model = "openrouter/free",
            tools = TOOLS,
            messages = conversation_history,
            tool_choice = "auto" 
            
        )

        if response.choices[0].message.tool_calls:
            conversation_history.append(response.choices[0].message)
            for tool_call in response.choices[0].message.tool_calls:
                
                name = tool_call.function.name
                args = tool_call.function.arguments

                result = run_tool(name, args)

                conversation_history.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                }
                )
            
        else:
            return response.choices[0].message.content

if __name__ == "__main__":
    while True:
        q = input("\nAsk (or 'exit'): ").strip()
        if q.lower() == "exit":
            break
        if q:
            print(run_agent(q))   
