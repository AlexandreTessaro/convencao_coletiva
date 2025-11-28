from sqlalchemy import Column, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.core.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    convencao_id = Column(UUID(as_uuid=True), ForeignKey("convencoes.id"), nullable=True)
    tipo = Column(String(50))  # NOVA_CONVENCAO, ATUALIZACAO, etc.
    titulo = Column(String(255))
    mensagem = Column(Text)
    lida = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="notifications")
    convencao = relationship("Convencao", back_populates="notifications")


class NotificationPreference(Base):
    __tablename__ = "notification_preferences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    email_enabled = Column(Boolean, default=True)
    push_enabled = Column(Boolean, default=True)
    frequencia = Column(String(20), default="IMEDIATO")  # IMEDIATO, DIARIO, SEMANAL
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="notification_preferences")

