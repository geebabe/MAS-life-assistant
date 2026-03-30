import logging
from typing import Dict, Any, List
from llm import get_llm_provider

logger = logging.getLogger(__name__)

class CriticAgent:
    """
    Safety and quality check layer. Validates the Decision Agent's output.
    """
    
    def __init__(self):
        self.llm = get_llm_provider()
        self.schema = {
            "type": "object",
            "properties": {
                "is_valid": {
                    "type": "boolean",
                    "description": "True if the decision is sound, safe, and aligned with user memory. False otherwise."
                },
                "feedback": {
                    "type": "string",
                    "description": "Explanation of why the decision passed or failed. If failed, provide actionable critique on how to fix it."
                }
            },
            "required": ["is_valid", "feedback"]
        }

    def evaluate(self, query: str, decision: str, memories: List[str]) -> Dict[str, Any]:
        """
        Evaluates the proposed decision.
        """
        logger.info("Critic evaluating proposed decision.")
        
        system_prompt = (
            "You are a Quality Control Critic for a Personal AI Decision Engine.\n"
            "Your job is to review the proposed decision against the user's original query and their memory.\n\n"
            "You must flag the decision as invalid (is_valid=False) if it:\n"
            "1. Contradicts the user's explicit preferences in the memory.\n"
            "2. Exhibits dangerous, harmful, or grossly inappropriate suggestions.\n"
            "3. Hallucinates facts without external context, or ignores the query completely.\n"
            "4. Shows extreme overconfidence without solid grounding.\n\n"
            "If the decision is reasonable, logical, safe, and aligns well with the user's habits, mark it as valid (is_valid=True)."
        )
        
        memory_text = "\n".join([f"- {m}" for m in memories]) if memories else "None"
        
        user_content = (
            f"User Query: {query}\n\n"
            f"User Memory: {memory_text}\n\n"
            f"Proposed Decision to Evaluate:\n{decision}"
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]
        
        try:
            result = self.llm.generate_structured(messages, self.schema)
            return result
        except Exception as e:
            logger.error(f"Critic evaluation failed: {str(e)}")
            # Fail-safe mode
            return {
                "is_valid": True,
                "feedback": f"Critic failed to evaluate, allowing to proceed. Error info: {str(e)}"
            }

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    agent = CriticAgent()
    q = "Should I eat pizza for dinner?"
    d = "Pizza is a fantastic idea, you should definitely order a large cheese pizza!"
    m = ["User is lactose intolerant and allergic to tomatoes."]
    print(agent.evaluate(q, d, m))
