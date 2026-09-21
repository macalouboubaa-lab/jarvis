from fastapi import APIRouter, Depends
from services.auth import AuthenticatedUser, get_current_user

router = APIRouter(prefix="/api/agents", tags=["Agents"])

@router.get("")
async def list_agents(
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    return [{"name": "Jarvis Core", "status": "active"}]
