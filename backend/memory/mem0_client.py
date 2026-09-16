from mem0 import Memory
from config import settings

def get_mem0_client() -> Memory:
    mem0_config = {
        "vector_store": {
            "provider": "supabase",
            "config": {
                "connection_string": settings.DATABASE_URL,
                "collection_name": "jarvis_memories"
            }
        },
        "llm": {
            "provider": "openai",
            "config": {
                "model": "gpt-4o-mini",
                "api_key": settings.OPENAI_API_KEY,
                "temperature": 0.2
            }
        },
        "embedder": {
            "provider": "openai",
            "config": {
                "model": "text-embedding-3-small",
                "api_key": settings.OPENAI_API_KEY
            }
        }
    }
    return Memory.from_config(mem0_config)

mem0_instance = get_mem0_client()
