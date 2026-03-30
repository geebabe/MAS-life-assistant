import logging
from typing import Dict, Any, Optional
from llm import get_llm_provider
from config import config

logger = logging.getLogger(__name__)

class IntentAgent:
    """
    Agent responsible for classifying user intent and determining if a web search is required.
    """
    
    def __init__(self):
        self.llm = get_llm_provider()
        self.schema = {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "enum": ["decision", "planning", "reflection", "info"],
                    "description": "The category of the user query."
                },
                "reasoning": {
                    "type": "string",
                    "description": "Short explanation for this classification."
                },
                "search_needed": {
                    "type": "boolean",
                    "description": "True if external search is needed for real-time context."
                },
                "search_query": {
                    "type": "string",
                    "description": "A refined search query if search_needed is true."
                }
            },
            "required": ["category", "reasoning", "search_needed"]
        }

    def classify(self, query: str) -> Dict[str, Any]:
        """
        Classifies the user query and decides on search intent.
        """
        system_prompt = (
            "You are an Intent Classifier for a Personal AI Decision Engine. "
            "Your job is to understand what the user wants and if they need real-time information.\n\n"
            "Categories:\n"
            "- decision: Choosing between options or deciding on an action.\n"
            "- planning: Organizing future activities or schedules.\n"
            "- reflection: Reviewing past experiences or habits.\n"
            "- info: General queries not related to personal choices.\n\n"
            "Decision Rule for search_needed:\n"
            "Set to true if the query is time-sensitive, requires real-time facts (weather, events, locations), "
            "or implies a need for external validation that memory alone cannot provide."
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"User Query: {query}"}
        ]
        
        logger.info(f"Classifying intent for query: {query}")
        try:
            result = self.llm.generate_structured(messages, self.schema)
            # If search_needed is true but search_query is missing, use the original query
            if result.get("search_needed") and not result.get("search_query"):
                result["search_query"] = query
            return result
        except Exception as e:
            logger.error(f"Intent classification failed: {str(e)}")
            # Fallback
            return {
                "category": "info",
                "reasoning": f"Fallback due to error: {str(e)}",
                "search_needed": False
            }

if __name__ == "__main__":
    # Quick test
    logging.basicConfig(level=logging.INFO)
    agent = IntentAgent()
    test_query = "Should I go to the night market tonight?"
    print(f"Query: {test_query}")
    print(f"Result: {agent.classify(test_query)}")
