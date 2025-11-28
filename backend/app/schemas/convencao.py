from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List
from uuid import UUID


class ConvencaoResponse(BaseModel):
    id: UUID
    instrumento_id: str
    titulo: Optional[str]
    tipo: Optional[str]
    data_publicacao: Optional[date]
    data_vigencia_inicio: Optional[date]
    data_vigencia_fim: Optional[date]
    sindicato_empregador: Optional[str]
    sindicato_trabalhador: Optional[str]
    municipio: Optional[str]
    uf: Optional[str]
    cnae: Optional[str]
    documento_url: Optional[str]
    formato_documento: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ConvencaoDetail(ConvencaoResponse):
    texto_extraido: Optional[str]
    documento_path: Optional[str]


class ConvencaoSearch(BaseModel):
    q: Optional[str] = None  # Busca geral
    cnpj: Optional[str] = None
    cnae: Optional[str] = None
    municipio: Optional[str] = None
    uf: Optional[str] = None
    keyword: Optional[str] = None  # Busca full-text
    page: int = 1
    page_size: int = 20

