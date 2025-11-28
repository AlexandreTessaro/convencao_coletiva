from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import List, Optional
from app.core.database import get_db
from app.models.user import User
from app.models.company import Company
from app.models.convencao import Convencao, ConvencaoEmpresa
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.convencao import ConvencaoResponse, ConvencaoDetail, ConvencaoSearch

router = APIRouter()


@router.get("/search", response_model=List[ConvencaoResponse])
async def search_convencoes(
    q: Optional[str] = Query(None),
    cnpj: Optional[str] = Query(None),
    cnae: Optional[str] = Query(None),
    municipio: Optional[str] = Query(None),
    uf: Optional[str] = Query(None),
    keyword: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search convenções"""
    query = db.query(Convencao)
    
    # Filter by user's companies if needed
    user_companies = db.query(Company).filter(Company.user_id == current_user.id).all()
    company_ids = [c.id for c in user_companies]
    
    # If user has companies, try to show convenções associated with them
    # But if no associations found or no companies, show all convenções (for testing)
    has_filters = any([q, cnpj, cnae, municipio, uf, keyword])
    
    if company_ids:
        # Get convenções associated with user's companies
        convencao_ids = db.query(ConvencaoEmpresa.convencao_id).filter(
            ConvencaoEmpresa.company_id.in_(company_ids)
        ).distinct().all()
        convencao_ids = [c[0] for c in convencao_ids]
        # Only filter by associations if we have associations AND no other filters
        # Otherwise, show all and let filters do the work
        if convencao_ids and not has_filters:
            query = query.filter(Convencao.id.in_(convencao_ids))
    # If no companies or no associations, show all convenções (filters will narrow down)
    
    # Apply filters
    if cnpj:
        # Search in metadata or by associated companies
        companies_with_cnpj = db.query(Company).filter(
            Company.cnpj == cnpj.replace(".", "").replace("/", "").replace("-", ""),
            Company.user_id == current_user.id
        ).all()
        if companies_with_cnpj:
            company_ids = [c.id for c in companies_with_cnpj]
            convencao_ids = db.query(ConvencaoEmpresa.convencao_id).filter(
                ConvencaoEmpresa.company_id.in_(company_ids)
            ).distinct().all()
            convencao_ids = [c[0] for c in convencao_ids]
            query = query.filter(Convencao.id.in_(convencao_ids))
        else:
            return []  # No companies found with this CNPJ
    
    if cnae:
        query = query.filter(Convencao.cnae == cnae)
    
    if municipio:
        query = query.filter(Convencao.municipio.ilike(f"%{municipio}%"))
    
    if uf:
        query = query.filter(Convencao.uf == uf.upper())
    
    if keyword:
        # Full-text search in texto_extraido
        query = query.filter(
            Convencao.texto_extraido.ilike(f"%{keyword}%")
        )
    
    if q:
        # General search
        query = query.filter(
            or_(
                Convencao.titulo.ilike(f"%{q}%"),
                Convencao.sindicato_empregador.ilike(f"%{q}%"),
                Convencao.sindicato_trabalhador.ilike(f"%{q}%"),
                Convencao.municipio.ilike(f"%{q}%")
            )
        )
    
    # Pagination
    total = query.count()
    offset = (page - 1) * page_size
    convencoes = query.order_by(Convencao.data_publicacao.desc()).offset(offset).limit(page_size).all()
    
    return convencoes


@router.get("/{convencao_id}", response_model=ConvencaoDetail)
async def get_convencao(
    convencao_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get convenção details"""
    # Check if user has access (through companies)
    user_companies = db.query(Company).filter(Company.user_id == current_user.id).all()
    company_ids = [c.id for c in user_companies]
    
    convencao = db.query(Convencao).filter(Convencao.id == convencao_id).first()
    
    if not convencao:
        raise HTTPException(
            status_code=404,
            detail="Convenção não encontrada"
        )
    
    # Check access
    if company_ids:
        has_access = db.query(ConvencaoEmpresa).filter(
            ConvencaoEmpresa.convencao_id == convencao.id,
            ConvencaoEmpresa.company_id.in_(company_ids)
        ).first()
        
        if not has_access:
            raise HTTPException(
                status_code=403,
                detail="Acesso negado a esta convenção"
            )
    
    return convencao


@router.get("/company/{company_id}", response_model=List[ConvencaoResponse])
async def get_company_convencoes(
    company_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get convenções for a specific company"""
    # Verify company belongs to user
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )
    
    # Get convenções
    convencao_ids = db.query(ConvencaoEmpresa.convencao_id).filter(
        ConvencaoEmpresa.company_id == company.id
    ).all()
    convencao_ids = [c[0] for c in convencao_ids]
    
    convencoes = db.query(Convencao).filter(Convencao.id.in_(convencao_ids)).order_by(
        Convencao.data_publicacao.desc()
    ).all()
    
    return convencoes

