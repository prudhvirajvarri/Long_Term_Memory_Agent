import chromadb
import uuid
import time
import os

client = chromadb.PersistentClient(path = "memory_db")

memory_collection = client.get_or_create_collection(
    name = "memory_collection",
    metadata = {"hnsw:space" : "cosine"}
)

#print(memory_collection)
"""
max_memory = 1

def get_file_size(file_path = "memory_db"):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(file_path):
        for filename in filenames:
            file_size = os.path.getsize(os.path.join(dirpath, filename))
            total_size += file_size
    # Convert size from bytesto GB
    total_size_gb = total_size / (1024 ** 3)
    return total_size_gb
"""

def create_memory(content: str):
    try:
        #while get_file_size() >= max_memory:
            #print("Memory limit reached. Deleting old memories.")
        if not content or not content.strip():
            return "Error creating memory: Content cannot be empty or whitespace."
          
        curr_time = time.time()
        memory_id = str(uuid.uuid4())
        memory_collection.add(
            ids = [memory_id],
            documents = [content],
            metadatas = [{
                "created_at": curr_time
            }]
        )
        
        print(f"Memory created with ID: {memory_id}")
        return "Memory created successfully."
    
    except Exception as e:
        return f"Error creating memory: {e}"
    
def retrieve_memory(query: str):
    try:
        results = memory_collection.query(
            query_texts = [query]
        )
        
        if not results or not results['documents'][0]:
            return "No relevant memory found."

        memory_retrieved = results['documents'][0][0]
        
        return f"Retrieved Memory: {memory_retrieved}"
    
    except Exception as e:
        return f"Error retrieving memory: {e}"

def delete_memory(query: str):
    try:
        results = memory_collection.query(
            query_texts = [query],
            n_results = 1,
            include=["documents", "distances"]
        )
        
        if not results or not results['documents'][0]:
            return "No relevant memory found to delete."
        
        distance = results['distances'][0][0]
        if distance > 0.9:
            return "No relevant memory found to delete."
        
        memory_id_to_delete = results['ids'][0][0]
        deleted_memory = results['documents'][0][0]
        memory_collection.delete(
            ids = [memory_id_to_delete]
        )
        
        return f"Deleted Memory: {deleted_memory} with ID: {memory_id_to_delete}"
    
    except Exception as e:
        return f"Error deleting memory: {e}"
    
