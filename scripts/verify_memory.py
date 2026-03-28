import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from memory.mem0_client import memory_manager
from config import config

def test_memory_crud():
    print(f"Testing Memory CRUD for user: {config.USER_ID}")
    
    # 1. Add a memory
    print("Adding memory...")
    text = "The user prefers working late at night in quiet environments."
    result = memory_manager.add_memory(text)
    print(f"Add result: {result}")
    
    # 2. Get all memories
    print("\nGetting all memories...")
    memories = memory_manager.get_memories()
    print(f"Found {len(memories)} memories.")
    for m in memories:
        print(f"- ID: {m['id']}, Content: {m['text']}")
    
    # 3. Search memory
    print("\nSearching memory for 'when does user work?'...")
    search_results = memory_manager.search_memory("when does user work?")
    print(f"Search results: {len(search_results)}")
    for res in search_results:
        print(f"- Content: {res['text']}, Score: {res.get('score', 'N/A')}")
        
    # 4. Delete a memory (clean up if possible, but we'll leave it for now to verify persistence if needed)
    # If memories is not empty, delete the first one
    if memories:
        mem_id = memories[0]['id']
        print(f"\nDeleting memory ID: {mem_id}")
        delete_result = memory_manager.delete_memory(mem_id)
        print(f"Delete result: {delete_result}")
        
        # Verify deletion
        new_memories = memory_manager.get_memories()
        print(f"Found {len(new_memories)} memories after deletion.")
        assert len(new_memories) < len(memories)

    print("\nMemory CRUD test completed successfully!")

if __name__ == "__main__":
    try:
        test_memory_crud()
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()
