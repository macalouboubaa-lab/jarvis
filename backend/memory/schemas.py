from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class MemoryItem(BaseModel):
    id: Optional[str] = None
    memory: str
    user_id: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: Optional[datetime] = None
