from openai import OpenAI
from dotenv import load_dotenv
from memory_manager import create_memory, retrieve_memory, delete_memory

import os
import json
import time

# load environment variables
load_dotenv()

# intialize OpenAI client
client = OpenAI()

# define tools

tools = [
    {
        "type": "function",
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
    },
    {
        "type": 'function',
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
    },
    {
        "type": "function",
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
]