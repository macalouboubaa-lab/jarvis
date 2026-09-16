from fastapi import APIRouter
router = APIRouter(prefix="/api/voice", tags=["Voice"])

@router.get("/status")
async def voice_status():
    return {"status": "ElevenLabs ready"}
