from fastapi import APIRouter
from memory.mem0_client import mem0_instance
from config import settings

router = APIRouter(prefix="/api/memory", tags=["Memory"])

@router.get("")
async def get_memories():
    return mem0_instance.get_all(user_id=settings.JARVIS_USER_ID)
