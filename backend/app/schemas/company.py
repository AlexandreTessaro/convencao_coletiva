from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional
from uuid import UUID


class CompanyCreate(BaseModel):
    cnpj: str
    razao_social: Optional[str] = None
    cnae: Optional[str] = None
    municipio: Optional[str] = None
    uf: Optional[str] = None

    @validator("cnpj")
    def validate_cnpj(cls, v):
        # Remove formatação
        cnpj = "".join(filter(str.isdigit, v))
        if len(cnpj) != 14:
            raise ValueError("CNPJ deve ter 14 dígitos")
        return cnpj

    @validator("cnae")
    def validate_cnae(cls, v):
        if v:
            # Remove formatação
            cnae = "".join(filter(str.isdigit, v))
            if len(cnae) != 7:
                raise ValueError("CNAE deve ter 7 dígitos")
            return cnae
        return v


class CompanyUpdate(BaseModel):
    razao_social: Optional[str] = None
    cnae: Optional[str] = None
    municipio: Optional[str] = None
    uf: Optional[str] = None


class CompanyResponse(BaseModel):
    id: UUID
    cnpj: str
    razao_social: Optional[str]
    cnae: Optional[str]
    municipio: Optional[str]
    uf: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

