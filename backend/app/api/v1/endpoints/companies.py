from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.user import User
from app.models.company import Company
from app.models.convencao import Convencao, ConvencaoEmpresa
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse

router = APIRouter()


@router.post("", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(
    company_data: CompanyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new company"""
    # Check if CNPJ already exists for this user
    existing = db.query(Company).filter(
        Company.user_id == current_user.id,
        Company.cnpj == company_data.cnpj
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empresa com este CNPJ já está cadastrada"
        )
    
    new_company = Company(
        user_id=current_user.id,
        **company_data.dict()
    )
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    
    # Associate existing convenções
    associate_convencoes_to_company(new_company, db)
    
    return new_company


@router.get("", response_model=List[CompanyResponse])
async def list_companies(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all companies for current user"""
    companies = db.query(Company).filter(Company.user_id == current_user.id).all()
    return companies


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get company details"""
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa não encontrada"
        )
    
    return company


@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: str,
    company_data: CompanyUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update company"""
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa não encontrada"
        )
    
    for key, value in company_data.dict(exclude_unset=True).items():
        setattr(company, key, value)
    
    db.commit()
    db.refresh(company)
    
    # Reassociate convenções if CNAE or municipio changed
    if company_data.cnae or company_data.municipio:
        associate_convencoes_to_company(company, db)
    
    return company


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete company"""
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa não encontrada"
        )
    
    db.delete(company)
    db.commit()
    return None


def associate_convencoes_to_company(company: Company, db: Session):
    """Associate relevant convenções to a company"""
    # Find convenções by CNAE
    convencoes_cnae = []
    if company.cnae:
        convencoes_cnae = db.query(Convencao).filter(Convencao.cnae == company.cnae).all()
    
    # Find convenções by municipio
    convencoes_municipio = []
    if company.municipio and company.uf:
        convencoes_municipio = db.query(Convencao).filter(
            Convencao.municipio == company.municipio,
            Convencao.uf == company.uf
        ).all()
    
    # Combine and remove duplicates
    all_convencoes = list(set(convencoes_cnae + convencoes_municipio))
    
    # Create associations
    for convencao in all_convencoes:
        existing = db.query(ConvencaoEmpresa).filter(
            ConvencaoEmpresa.convencao_id == convencao.id,
            ConvencaoEmpresa.company_id == company.id
        ).first()
        
        if not existing:
            score = calculate_relevancia_score(convencao, company)
            association = ConvencaoEmpresa(
                convencao_id=convencao.id,
                company_id=company.id,
                relevancia_score=score
            )
            db.add(association)
    
    db.commit()


def calculate_relevancia_score(convencao: Convencao, company: Company) -> float:
    """Calculate relevance score between convenção and company"""
    score = 0.0
    
    if convencao.cnae == company.cnae:
        score += 50.0
    
    if convencao.municipio == company.municipio and convencao.uf == company.uf:
        score += 50.0
    
    return score

