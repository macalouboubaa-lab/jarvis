import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from agent.core import ask_jarvis, to_langchain_messages
from database import supabase
from services.auth import AuthenticatedUser, get_current_user

router = APIRouter(prefix="/api/chat", tags=["Chat"])
logger = logging.getLogger(__name__)

class ChatMessageRequest(BaseModel):
    message: str = Field(..., min_length=1)
    conversation_id: Optional[str] = None

class ChatMessageResponse(BaseModel):
    response: str
    conversation_id: str
    created_at: str

@router.post("", response_model=ChatMessageResponse)
async def post_chat_message(
    payload: ChatMessageRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    try:
        conv_id = payload.conversation_id or "default-session"
        history_response = (
            supabase.table("chat_history")
            .select("sender, content, created_at")
            .eq("conversation_id", conv_id)
            .eq("user_id", current_user.id)
            .order("created_at", desc=True)
            .limit(10)
            .execute()
        )
        if history_response.error:
            raise RuntimeError("Unable to load chat history.")

        history = to_langchain_messages(
            list(reversed(history_response.data or []))
        )

        user_insert_response = supabase.table("chat_history").insert({
            "conversation_id": conv_id,
            "sender": "user",
            "content": payload.message,
            "user_id": current_user.id,
            "created_at": datetime.utcnow().isoformat()
        }).execute()
        if user_insert_response.error:
            raise RuntimeError("Unable to persist user message.")

        bot_reply = await ask_jarvis(
            payload.message,
            user_id=current_user.id,
            history=history,
        )

        now_iso = datetime.utcnow().isoformat()
        assistant_insert_response = supabase.table("chat_history").insert({
            "conversation_id": conv_id,
            "sender": "assistant",
            "content": bot_reply,
            "user_id": current_user.id,
            "created_at": now_iso
        }).execute()
        if assistant_insert_response.error:
            raise RuntimeError("Unable to persist assistant message.")

        return ChatMessageResponse(
            response=bot_reply,
            conversation_id=conv_id,
            created_at=now_iso
        )
    except Exception:
        logger.exception("Chat request failed")
        raise HTTPException(
            status_code=500,
            detail="Une erreur interne est survenue.",
        )
