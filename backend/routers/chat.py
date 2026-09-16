from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from agent.core import ask_jarvis
from database import supabase
from config import settings

router = APIRouter(prefix="/api/chat", tags=["Chat"])

class ChatMessageRequest(BaseModel):
    message: str = Field(..., min_length=1)
    conversation_id: Optional[str] = None

class ChatMessageResponse(BaseModel):
    response: str
    conversation_id: str
    created_at: str

@router.post("", response_model=ChatMessageResponse)
async def post_chat_message(payload: ChatMessageRequest):
    try:
        conv_id = payload.conversation_id or "default-session"
        supabase.table("chat_history").insert({
            "conversation_id": conv_id,
            "sender": "user",
            "content": payload.message,
            "user_id": settings.JARVIS_USER_ID,
            "created_at": datetime.utcnow().isoformat()
        }).execute()

        bot_reply = await ask_jarvis(payload.message)

        now_iso = datetime.utcnow().isoformat()
        supabase.table("chat_history").insert({
            "conversation_id": conv_id,
            "sender": "assistant",
            "content": bot_reply,
            "user_id": settings.JARVIS_USER_ID,
            "created_at": now_iso
        }).execute()

        return ChatMessageResponse(
            response=bot_reply,
            conversation_id=conv_id,
            created_at=now_iso
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
