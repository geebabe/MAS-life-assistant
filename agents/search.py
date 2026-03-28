import os
import logging
from typing import List, Dict, Any, Optional
from config import config

try:
    from tavily import TavilyClient
except ImportError:
    TavilyClient = None

logger = logging.getLogger(__name__)

class SearchAgent:
    """
    Agent responsible for fetching real-time external knowledge using Tavily.
    Takes a refined query and returns a clean, LLM-ready text string built from search snippets.
    """
    
    def __init__(self):
        """Initializes the Tavily client securely using environment variables."""
        self.api_key = config.TAVILY_API_KEY
        
        if not self.api_key:
            logger.warning("TAVILY_API_KEY not found in environment. Web search will be disabled.")
            self.client = None
        elif TavilyClient is None:
            logger.warning("tavily-python not installed. Run `pip install tavily-python` to use web search.")
            self.client = None
        else:
            self.client = TavilyClient(api_key=self.api_key)

    def search(self, query: str, max_results: int = 4) -> str:
        """
        Executes a web search and formats the response for LLM context.
        
        Args:
            query (str): The search query strings.
            max_results (int): Maximum number of search sources to return.
            
        Returns:
            str: Filtered and formatted snippets containing real-time web context.
        """
        if not self.client:
            return "System Note: Web search is temporarily unavailable (Missing API Key or tavily-python library)."
            
        logger.info(f"Tavily searching for: '{query}'")
        
        try:
            # Perform search. Using include_answer=True helps get a direct concise answer alongside snippets
            response = self.client.search(
                query=query,
                search_depth="basic",  # 'basic' is fast, 'advanced' is deeper but slower
                max_results=max_results,
                include_answer=True,
                include_raw_content=False,
                include_images=False
            )
            
            snippets = []
            
            # Start with the synthesized answer if Tavily provided one
            if response.get("answer"):
                snippets.append(f"--- Quick AI Summary ---\n{response['answer']}\n")
            
            # Accumulate relevant snippets from the top documents
            if response.get("results"):
                snippets.append("--- Search Results ---")
                for i, result in enumerate(response['results'], 1):
                    title = result.get('title', 'Unknown Title')
                    url = result.get('url', 'No URL')
                    content = result.get('content', '')
                    
                    # Formatting cleanly for LLM consumption
                    snippet_block = f"Source [{i}]: {title}\nURL: {url}\nDetails: {content}\n"
                    snippets.append(snippet_block)
            
            if not snippets:
                return f"No useful web information found for the query: '{query}'"
                
            # Join all snippets with newlines
            return "\n".join(snippets).strip()
            
        except Exception as e:
            error_msg = f"Search attempt failed with error: {str(e)}"
            logger.error(error_msg)
            return error_msg
