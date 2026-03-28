import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
    DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
    
    # Mem0 Configuration
    USER_ID = "default_user"
    MEM0_CONFIG = {
        "llm": {
            "provider": "gemini",
            "config": {
                "model": "gemini-2.5-flash",
                "api_key": os.getenv("GOOGLE_API_KEY"),
            }
        },
        "embedder": {
            "provider": "huggingface",
            "config": {
                "model": "sentence-transformers/all-MiniLM-L6-v2",
            }
        },
        "vector_store": {
            "provider": "qdrant",
            "config": {
                "path": os.path.join(os.getcwd(), ".mem0/qdrant"),
            }
        },
        "history_db": os.path.join(os.getcwd(), ".mem0/history.db")
    }

config = Config()
