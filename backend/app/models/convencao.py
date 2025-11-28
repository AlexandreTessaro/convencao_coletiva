from sqlalchemy import Column, String, Date, Text, ForeignKey, DateTime, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.core.database import Base


class Convencao(Base):
    __tablename__ = "convencoes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    instrumento_id = Column(String(50), unique=True, nullable=False, index=True)
    titulo = Column(String(500))
    tipo = Column(String(50))  # CCT, ACT, etc.
    data_publicacao = Column(Date, index=True)
    data_vigencia_inicio = Column(Date, index=True)
    data_vigencia_fim = Column(Date, index=True)
    sindicato_empregador = Column(String(255))
    sindicato_trabalhador = Column(String(255))
    municipio = Column(String(100), index=True)
    uf = Column(String(2), index=True)
    cnae = Column(String(7), index=True)
    documento_url = Column(Text)
    documento_path = Column(Text)
    texto_extraido = Column(Text)  # Limitado a 1MB no código
    formato_documento = Column(String(20))  # HTML, PDF_DIGITAL, PDF_ESCANEADO
    status = Column(String(20), default="PROCESSANDO")  # PROCESSANDO, PROCESSADO, ERRO
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    empresas = relationship("ConvencaoEmpresa", back_populates="convencao", cascade="all, delete-orphan")
    metadados = relationship("ConvencaoMetadata", back_populates="convencao", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="convencao")


class ConvencaoEmpresa(Base):
    __tablename__ = "convencoes_empresas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    convencao_id = Column(UUID(as_uuid=True), ForeignKey("convencoes.id"), nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    relevancia_score = Column(DECIMAL(5, 2))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    convencao = relationship("Convencao", back_populates="empresas")
    company = relationship("Company", back_populates="convencoes")


class ConvencaoMetadata(Base):
    __tablename__ = "convencoes_metadados"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    convencao_id = Column(UUID(as_uuid=True), ForeignKey("convencoes.id"), nullable=False)
    chave = Column(String(100), nullable=False, index=True)
    valor = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    convencao = relationship("Convencao", back_populates="metadados")

