import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import chat, memory

app = FastAPI(
    title="MAS Life Assistant API",
    description="API for the Multi-Agent System (MAS) Life Assistant powered by LangGraph and Mem0",
    version="1.0.0"
)

# CORS middleware for potential frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    return {"status": "healthy", "message": "MAS Life Assistant API is running"}

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(memory.router, prefix="/api/memory", tags=["memory"])

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
