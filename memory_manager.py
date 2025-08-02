import chromadb
import uuid
import time

client = chromadb.PersistentClient(path = "memory_db")

memory_collection = client.get_or_create_collection(
    name = "memory_collection",
    metadata = {
        "hnsw": {
            "space" : "cosine"
        }
    }
)
# max_memory = 10

def create_memory(content: str):
    try:
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
            query_texts = [query]
        )
        
        if not results or not results['documents'][0]:
            return "No relevant memory found to delete."
        
        memory_id_to_delete = results['ids'][0][0]
        deleted_memory = results['documents'][0][0]
        memory_collection.delete(
            ids = [memory_id_to_delete]
        )
        
        return f"Deleted Memory: {deleted_memory} with ID: {memory_id_to_delete}"
    
    except Exception as e:
        return f"Error deleting memory: {e}"
    
