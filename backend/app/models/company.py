from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.core.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    cnpj = Column(String(14), nullable=False, index=True)
    razao_social = Column(String(255))
    cnae = Column(String(7), index=True)
    municipio = Column(String(100), index=True)
    uf = Column(String(2), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="companies")
    convencoes = relationship("ConvencaoEmpresa", back_populates="company", cascade="all, delete-orphan")

