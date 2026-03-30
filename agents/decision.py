import logging
from typing import List, Optional
from llm import get_llm_provider

logger = logging.getLogger(__name__)

class DecisionAgent:
    """
    The 'brain' of the system that fuses user query, retrieved memories,
    and external knowledge to produce a personalized recommendation.
    """
    
    def __init__(self):
        self.llm = get_llm_provider()

    def decide(self, query: str, memories: List[str], external_context: Optional[str] = None, critic_feedback: Optional[str] = None) -> str:
        """
        Generates a final decision/recommendation based on memory and (optional) search context.
        """
        logger.info(f"Generating decision for query: '{query}'")
        
        system_prompt = (
            "You are a Personal AI Decision Assistant. "
            "Your job is to provide highly personalized, highly relevant recommendations based on the user's past habits and current external facts.\n\n"
            "Guidelines:\n"
            "1. Transparent Reasoning: Always explain *why* you are making the suggestion. "
            "Connect the user's past behaviors/preferences (Memory) to your recommendation.\n"
            "2. Integration: If External Context is provided, fuse it with the Memory to form a logical conclusion.\n"
            "3. Tone: Helpful, direct, and slightly analytical.\n"
            "4. Format: State your reasoning clearly, followed by the specific recommendation."
        )
        
        # Format the memory section
        memory_text = "\n".join([f"- {m}" for m in memories]) if memories else "No relevant past preferences available."
        
        user_content = f"User Query: {query}\n\nUser Memory / Preferences:\n{memory_text}"
        
        # Check if we got something useful from Tavily
        if external_context and not external_context.startswith("System Note: Web search is temporarily unavailable") and not external_context.startswith("No useful web information"):
            user_content += f"\n\nExternal Context (Real-time facts):\n{external_context}"
            
        if critic_feedback:
            logger.info("Applying critic feedback to decision generation.")
            user_content += f"\n\nCRITIQUE OF PREVIOUS DECISION (Please modify your answer to address this):\n{critic_feedback}"
            
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]
        
        try:
            result = self.llm.generate_with_messages(messages)
            return result
        except Exception as e:
            logger.error(f"Decision generation failed: {str(e)}")
            return f"I apologize, but I encountered an error while trying to form a decision: {str(e)}"

if __name__ == "__main__":
    # Quick test
    logging.basicConfig(level=logging.INFO)
    agent = DecisionAgent()
    test_query = "Should I study at home or go to a cafe?"
    test_mems = ["Prefers quiet environments for deep work.", "Finds home too distracting with roommates."]
    print(agent.decide(test_query, test_mems))
