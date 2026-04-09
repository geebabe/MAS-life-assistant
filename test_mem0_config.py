import os
from config import config
from mem0 import Memory
import logging

# Set logging to see what mem0 is doing
logging.basicConfig(level=logging.DEBUG)

def test_config():
    print("Testing Mem0 Config...")
    try:
        memory = Memory.from_config(config.MEM0_CONFIG)
        print("Memory initialized successfully.")
        
        # Try to add a test memory
        print("\nAttempting to add memory...")
        memory.add("Testing memory storage", user_id="test_user")
        print("Memory added successfully.")
        
        # Try to search
        print("\nAttempting to search memory...")
        results = memory.search("Testing", user_id="test_user")
        print(f"Search successful. Found {len(results)} results.")
        
    except Exception as e:
        print(f"\nCaught Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_config()
