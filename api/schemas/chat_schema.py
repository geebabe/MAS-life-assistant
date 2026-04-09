from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ChatRequest(BaseModel):
    query: str
    user_id: str = "default_user"

class ChatResponse(BaseModel):
    query: str
    user_id: str
    decision: str
    intent_category: Optional[str] = None
    search_needed: bool = False
    search_query: Optional[str] = None
    memories: List[str] = []
    external_context: Optional[str] = None
    is_valid: bool = True
    critic_feedback: Optional[str] = None
    revision_count: int = 0
    insights: List[str] = []
