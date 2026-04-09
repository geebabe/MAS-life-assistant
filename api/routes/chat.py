from fastapi import APIRouter, HTTPException
from api.schemas.chat_schema import ChatRequest, ChatResponse
from graph.workflow import run_workflow

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    try:
        final_state = run_workflow(request.query, user_id=request.user_id)
        
        # Mapping final_state (TypedDict) to ChatResponse (Pydantic)
        return ChatResponse(
            query=final_state.get("query"),
            user_id=final_state.get("user_id"),
            decision=final_state.get("decision", "No decision made."),
            intent_category=final_state.get("intent_category"),
            search_needed=final_state.get("search_needed", False),
            search_query=final_state.get("search_query"),
            memories=final_state.get("memories", []),
            external_context=final_state.get("external_context"),
            is_valid=final_state.get("is_valid", True),
            critic_feedback=final_state.get("critic_feedback"),
            revision_count=final_state.get("revision_count", 0),
            insights=final_state.get("insights", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
