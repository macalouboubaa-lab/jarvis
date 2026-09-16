from fastapi import APIRouter
router = APIRouter(prefix="/api/agents", tags=["Agents"])

@router.get("")
async def list_agents():
    return [{"name": "Jarvis Core", "status": "active"}]
