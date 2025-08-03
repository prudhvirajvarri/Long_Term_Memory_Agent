from openai import OpenAI
from dotenv import load_dotenv
from memory_manager import create_memory, retrieve_memory, delete_memory

import os
import json
import time

# load environment variables
load_dotenv()

# initialize OpenAI client
client = OpenAI()

# define tools

tools = [
    {
        "type": "function",
        "function":{
            "name": "create_memory",
            "description": "Creates a new memory to store new information or facts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The content of the memory to be created. This should contain the information or fact to be stored."
                    }
                },
                "required": ["content"]
            }
        }
    },
    {
        "type": 'function',
        "function": {
            "name": "retrieve_memory",
            "description": "Retrieves a memory based on the user's query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query to search for relevant memories."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_memory",
            "description": "Deletes a memory based on the user's query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query to delete a relevant memory."
                    }
                },
                "required": ["query"]
            }
        }
    }
]

functions = {
    "create_memory": create_memory,
    "retrieve_memory": retrieve_memory,
    "delete_memory": delete_memory
}

def conversation_loop():
    messages = [
        {
             "role": "system",
             "content": "You are a helpful assistant that can create, retrieve, and delete memories."
        }
    ]
    
    print("AI assistant is ready to chat. Type 'exit' or 'quit' to end the conversation.")
    while True: 
        user_input = input("You: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the conversation. Goodbye!")
            break
        
        messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )
        
        response = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = messages,
            tools = tools,
            tool_choice = "auto"
        )
        #print(response)
        response_message = response.choices[0].message
        messages.append(response_message)
        
        tool_calls = response.choices[0].message.tool_calls
        #print("Tool Calls:", tool_calls)
        if tool_calls:
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = functions[function_name]
                function_args = tool_call.function.arguments
                
                functions_response = function_to_call(**json.loads(function_args))
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": functions_response,
                        "name": function_name
                    }
                )
        
            second_api_response = client.chat.completions.create(
                model = "gpt-4o-mini",
                messages = messages
            )
            #print(second_api_response)
            final_message = second_api_response.choices[0].message
            print(f"AI: {final_message.content}")
            messages.append(final_message)
        else:
            final_message = response_message
            print(f"AI: {final_message.content}")

        
if __name__ == "__main__":
    conversation_loop()