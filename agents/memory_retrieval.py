import logging
from typing import List, Dict, Any
from memory.mem0_client import memory_manager

logger = logging.getLogger(__name__)

class MemoryRetrievalAgent:
    """
    Agent responsible for fetching relevant past preferences and decisions from mem0.
    """
    
    def __init__(self):
        self.memory_manager = memory_manager

    def retrieve(self, query: str, user_id: str = None, limit: int = 5) -> List[str]:
        """
        Retrieves relevant memories based on the user's current query.
        """
        logger.info(f"Retrieving memories for: '{query}'")
        try:
            # search_memory returns a list of results, each containing 'memory' (the text) and 'id'
            results = self.memory_manager.search_memory(query, user_id=user_id, limit=limit)
            
            # Extract the raw memory text if available, or just convert result to string
            memories = []
            if isinstance(results, list):
                for res in results:
                    # Depending on mem0 result format, it could be a dict or a result object
                    if isinstance(res, dict) and 'memory' in res:
                        memories.append(res['memory'])
                    else:
                        memories.append(str(res))
            
            if not memories:
                logger.info("No relevant memories found.")
                return ["No relevant past preferences found in memory."]
                
            return memories
            
        except Exception as e:
            logger.error(f"Memory retrieval failed: {str(e)}")
            return [f"Error retrieving memories: {str(e)}"]

if __name__ == "__main__":
    # Quick test
    logging.basicConfig(level=logging.INFO)
    agent = MemoryRetrievalAgent()
    test_query = "Should I study at home?"
    print(f"Results: {agent.retrieve(test_query)}")
