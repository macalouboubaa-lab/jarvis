from fastapi import APIRouter, Depends
from memory.mem0_client import mem0_instance
from services.auth import AuthenticatedUser, get_current_user

router = APIRouter(prefix="/api/memory", tags=["Memory"])

@router.get("")
async def get_memories(
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    return mem0_instance.get_all(user_id=current_user.id)
