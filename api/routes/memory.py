from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from memory.mem0_client import memory_manager

router = APIRouter()

class MemoryAddRequest(BaseModel):
    text: str
    user_id: Optional[str] = None

class MemorySearchRequest(BaseModel):
    query: str
    user_id: Optional[str] = None
    limit: int = 5

@router.post("/add")
async def add_memory(request: MemoryAddRequest):
    try:
        result = memory_manager.add_memory(request.text, user_id=request.user_id)
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search")
async def search_memory(request: MemorySearchRequest):
    try:
        results = memory_manager.search_memory(request.query, user_id=request.user_id, limit=request.limit)
        return {"success": True, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all/{user_id}")
async def get_all_memories(user_id: str):
    try:
        results = memory_manager.get_memories(user_id=user_id)
        return {"success": True, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/all/{user_id}")
async def delete_all_memories(user_id: str):
    try:
        memory_manager.delete_all_memories(user_id=user_id)
        return {"success": True, "message": f"All memories for user {user_id} deleted."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
