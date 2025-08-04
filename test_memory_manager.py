import pytest
import chromadb
from memory_manager import create_memory, retrieve_memory, delete_memory

@pytest.fixture
def memory_collection_for_testing():
    client = chromadb.Client(
        settings=chromadb.Settings(allow_reset=True, is_persistent=False)
    )
    collection = client.get_or_create_collection(name="test_collection")
    
    import memory_manager
    original_collection = memory_manager.memory_collection
    memory_manager.memory_collection = collection
    
    yield collection
    client.reset() 
    
    memory_manager.memory_collection = original_collection

def test_memory_lifecycle(memory_collection_for_testing):
    creation_response = create_memory("I use Shram and Magnet as productivity tools.")
    assert creation_response == "Memory created successfully."
    assert memory_collection_for_testing.count() == 1
    retrieval_response = retrieve_memory("What are the productivity tools that I use?")
    assert "Retrieved Memory: I use Shram and Magnet as productivity tools." in retrieval_response
    delete_response = delete_memory("I don't use Magnet anymore.")
    assert "Deleted Memory: I use Shram and Magnet as productivity tools." in delete_response
    assert memory_collection_for_testing.count() == 0

def test_retrieve_non_existent_memory(memory_collection_for_testing):
    response = retrieve_memory("What is my favorite color?")
    assert response == "No relevant memory found."

@pytest.mark.parametrize(
    "content_to_test, is_valid",
    [
        ("", False),
        ("   ", False),
        ("!@#$%", True),
        ("这是一个中文记忆", True)
    ]
)
def test_create_memory_with_various_content(memory_collection_for_testing, content_to_test, is_valid):
    creation_response = create_memory(content_to_test)
    
    if is_valid:
        assert creation_response == "Memory created successfully."
        results = memory_collection_for_testing.query(query_texts=[content_to_test], n_results=1)
        assert results['documents'][0][0] == content_to_test
    else:
        assert creation_response == "Error creating memory: Content cannot be empty or whitespace."
        assert memory_collection_for_testing.count() == 0

def test_retrieve_ambiguous_query(memory_collection_for_testing):
    create_memory("My car is a red sedan.")
    create_memory("My favorite fruit is a red apple.")
    retrieval_response = retrieve_memory("what kind of vehicle do I own?")
    assert "car" in retrieval_response
    assert "apple" not in retrieval_response
    
def test_delete_non_existent_memory(memory_collection_for_testing):
    create_memory("My pet's name is Sparky.")
    response = delete_memory("What is the capital of Mars?")
    assert response == "No relevant memory found to delete."
    assert memory_collection_for_testing.count() == 1