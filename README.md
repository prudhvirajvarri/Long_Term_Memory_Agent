# LONG_TERM_MEMORY_AGENT

The goal of this project is to create a long term memory system for GPT. It will be a tool that works with OpenAI APIs to help the chatbot remember important information during long conversations. This system will be able to create, retrieve, and delete memories, so the chatbot can keep track of past messages and respond more accurately over time.

## Features

* **Create Memories:** Tell the agent to remember information or facts.
* **Retrieve Memories:** Ask the agent questions related to past information or facts you have given.
* **Delete Memories:** Tell the agent to forget information or facts.

---

## Design Decisions

1. **Memory Storage:**
   I chose ChromaDB as a local vector database to store, retrieve and delete memory. Used persistent storage (PersistentClient) for long term memory management.
    * Used cosine similarity as the distance metric for semantic similarity search, which helps to retrieve relevant memory even if the query phrases are different.

2. **Tool Calling:**
   I used the OpenAI tool's calling feature to connect the model with my memory management function.
    * I defined the tools **create_memory**, **retrieve_memory**, **delete_memory** and let the model decide by itself to call the required function based on what the user says.

3. **Model Selection:**
   I used the **gpt-4o-mini** model.
    * It is fast, handles tools well and is cheaper to run.

4. **Safe deletion:**
   I added a similarity check in the delete_memory function.
    * If the distance is more than 0.9, the memory won't be deleted. This will avoid deleting unrelated memories.

5. **Future Improvements:**
   I want to set a limit on how much space the memory can use. This is to make sure it doesn't take up all the free space on the system.
    * I already added timestamp(created_at) in the Metadata, which helps track older memories.
    * In the future, when storage is full, I plan to take the old memories and pass them to the model to summarise.
    * The summarised version will take less space and still keep the important information.

---

## Setup & Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/prudhvirajvarri/Long_Term_Memory_Agent.git
    cd LONG_TERM_MEMORY_AGENT
    ```

2. **Create a virtual environment:**
   ```bash
   # On Windows
   python -m venv long_term_memory
   long_term_memory\Scripts\activate

   # On macOS/Linux
   python3 -m venv long_term_memory
   source long_term_memory/bin/activate

   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key:**
   Create a file named '.env' in this add your OpenAI API key:
   ```
   OPENAI_API_KEY = "your_API_key"
   ```
---

## Running Tests
I have included test files to check if the memory functions and tool calling logic are working correctly.
1. **Install testing dependencies:**
   ```bash
   pip install pytest
   ```
2. **Run all tests:**
   ```bash
   pytest
   ```

---

# How to Run

Open your terminal:

```bash
python main.py
```

---

# Example Conversation

```

AI assistant is ready to chat. Type 'exit' or 'quit' to end the conversation.
You: Hi
AI: Hello! How can I assist you today?
You: My name is Prudhviraj.
Memory created with ID: 8fb54236-6d04-4fa4-b358-365165ed752f
AI: Nice to meet you, Prudhviraj! How can I help you today?
You: I use Shram and Magnet as productivity tools.
Memory created with ID: a147f5e3-8e70-40eb-b973-6c488bd70b04
Memory created with ID: da2d733c-e93b-48eb-84aa-c2fb9bba83a0
AI: Got it! I’ve noted that you use Shram and Magnet as productivity tools. How do you find them helpful?
You: What are the productivity tools that I use?
AI: You use Shram and Magnet as productivity tools. If you need tips or help related to them, feel free to ask!
You: I don't use Magnet anymore.
AI: I've removed Magnet from your memory. Now, you only have Shram noted as your productivity tool. If there's anything else you'd like to update or add, just let me know!
You: What are the productivity tools that I use?
AI: You currently use Shram as your productivity tool. If you have any questions or need assistance with it, feel free to ask!
You: What is my name?
AI: Your name is Prudhviraj. How can I assist you further?
You: 
AI: It seems like your message may not have come through. How can I help you today?
You: delete my name.
AI: I've removed your name from memory. If there's anything else you'd like me to do, just let me know!
You: What is my name?
AI: It seems I no longer have your name stored in memory. Would you like to tell me your name again?
You: What is my favourite food?
AI: I don't have any information about your favourite food at the moment. If you'd like to share it, I can remember it for you!
You: exit
Exiting the conversation. Goodbye!

```