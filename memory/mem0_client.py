from mem0 import Memory
from config import config
import os

class MemoryManager:
    def __init__(self):
        # Configure mem0 with local storage paths
        self.memory = Memory.from_config(config.MEM0_CONFIG)

    def add_memory(self, text: str, user_id: str = None):
        """Adds a new memory for the user."""
        user_id = user_id or config.USER_ID
        return self.memory.add(text, user_id=user_id)

    def search_memory(self, query: str, user_id: str = None, limit: int = 5):
        """Searches for relevant memories."""
        user_id = user_id or config.USER_ID
        return self.memory.search(query, user_id=user_id, limit=limit)

    def get_memories(self, user_id: str = None):
        """Returns all memories for the user."""
        user_id = user_id or config.USER_ID
        return self.memory.get_all(user_id=user_id)

    def delete_memory(self, memory_id: str, user_id: str = None):
        """Deletes a specific memory by its ID."""
        user_id = user_id or config.USER_ID
        return self.memory.delete(memory_id, user_id=user_id)

    def delete_all_memories(self, user_id: str = None):
        """Deletes all memories for a user."""
        user_id = user_id or config.USER_ID
        return self.memory.delete_all(user_id=user_id)

# Singleton instance
memory_manager = MemoryManager()
