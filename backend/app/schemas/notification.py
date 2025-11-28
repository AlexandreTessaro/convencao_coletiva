from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID


class NotificationResponse(BaseModel):
    id: UUID
    tipo: str
    titulo: str
    mensagem: Optional[str]
    lida: bool
    convencao_id: Optional[UUID]
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationPreferenceUpdate(BaseModel):
    email_enabled: Optional[bool] = None
    push_enabled: Optional[bool] = None
    frequencia: Optional[str] = None  # IMEDIATO, DIARIO, SEMANAL

