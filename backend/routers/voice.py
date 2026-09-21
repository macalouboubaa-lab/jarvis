from fastapi import APIRouter, Depends
from services.auth import AuthenticatedUser, get_current_user

router = APIRouter(prefix="/api/voice", tags=["Voice"])

@router.get("/status")
async def voice_status(
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    return {"status": "ElevenLabs ready"}
