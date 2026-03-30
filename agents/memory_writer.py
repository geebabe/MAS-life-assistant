import logging
from typing import Dict, Any, List
from llm import get_llm_provider
from memory.mem0_client import memory_manager

logger = logging.getLogger(__name__)

class MemoryWriterAgent:
    """
    Agent responsible for extracting long-term insights and updating mem0.
    """
    
    def __init__(self):
        self.llm = get_llm_provider()
        self.memory_manager = memory_manager
        self.schema = {
            "type": "object",
            "properties": {
                "insights": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "A list of distinct, concise facts, preferences, or habits learned about the user from the interaction. Empty if nothing new is learned."
                }
            },
            "required": ["insights"]
        }

    def write(self, query: str, decision: str, user_feedback: str = None, user_id: str = None) -> List[str]:
        """
        Analyzes the interaction and saves any new insights to memory.
        """
        logger.info("Analyzing interaction for new memory insights.")
        
        system_prompt = (
            "You are the Memory Extraction Module for a Personal AI Assistant.\n"
            "Your goal is to extract new, long-term facts, preferences, habits, or behavioral signals about the user.\n\n"
            "Rules:\n"
            "- Only extract facts about the *user*, not general world facts.\n"
            "- Keep extraction concise and declarative (e.g., 'Prefers quiet working spaces', 'Dislikes overly optimistic advice').\n"
            "- If there is nothing distinctly new or relevant to infer about the user's habits/preferences, return an empty list.\n"
            "- Pay special attention to 'User Feedback' if provided, as it usually indicates a strong preference or correction."
        )
        
        user_content = f"User Query: {query}\n\nAssistant Decision: {decision}"
        if user_feedback:
            user_content += f"\n\nUser Feedback: {user_feedback}"
            
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]
        
        try:
            result = self.llm.generate_structured(messages, self.schema)
            # Ensure it's a list even if parsing goes slightly wrong
            insights = result.get("insights", []) if isinstance(result, dict) else []
            
            # Save to mem0
            for insight in insights:
                logger.info(f"Saving new memory: '{insight}'")
                self.memory_manager.add_memory(insight, user_id=user_id)
                
            return insights
            
        except Exception as e:
            logger.error(f"Memory extraction failed: {str(e)}")
            return []

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    agent = MemoryWriterAgent()
    q = "I want to start running but my knees hurt in the cold."
    d = "You should try indoor swimming or an indoor track."
    f = "Good idea, I like swimming but I hate crowded pools."
    print("Extracted insights:", agent.write(q, d, f))
