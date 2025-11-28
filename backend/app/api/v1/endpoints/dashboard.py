from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.user import User
from app.models.company import Company
from app.models.convencao import Convencao, ConvencaoEmpresa
from app.models.notification import Notification
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()


@router.get("/stats")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics"""
    # Count companies
    total_companies = db.query(Company).filter(Company.user_id == current_user.id).count()
    
    # Count convenções
    company_ids = db.query(Company.id).filter(Company.user_id == current_user.id).all()
    company_ids = [c[0] for c in company_ids]
    
    total_convencoes = 0
    novas_convencoes = 0
    if company_ids:
        convencao_ids = db.query(ConvencaoEmpresa.convencao_id).filter(
            ConvencaoEmpresa.company_id.in_(company_ids)
        ).distinct().all()
        convencao_ids = [c[0] for c in convencao_ids]
        
        total_convencoes = len(convencao_ids)
        
        # Count new convenções (last 7 days)
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        novas_convencoes = db.query(Convencao).filter(
            Convencao.id.in_(convencao_ids),
            Convencao.created_at >= seven_days_ago
        ).count()
    
    # Count unread notifications
    unread_notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.lida == False
    ).count()
    
    # Count dissidio alerts (unread)
    dissidio_types = [
        'VENCIMENTO_PROXIMO_90',
        'VENCIMENTO_PROXIMO_60',
        'VENCIMENTO_PROXIMO_30',
        'VENCIMENTO_URGENTE_15',
        'VENCIMENTO_URGENTE_7',
        'VENCIDO'
    ]
    dissidio_alerts_count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.tipo.in_(dissidio_types),
        Notification.lida == False
    ).count()
    
    return {
        "total_companies": total_companies,
        "total_convencoes": total_convencoes,
        "novas_convencoes": novas_convencoes,
        "unread_notifications": unread_notifications,
        "dissidio_alerts_count": dissidio_alerts_count
    }


@router.get("/recent")
async def get_recent_convencoes(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get recent convenções"""
    company_ids = db.query(Company.id).filter(Company.user_id == current_user.id).all()
    company_ids = [c[0] for c in company_ids]
    
    if not company_ids:
        return []
    
    convencao_ids = db.query(ConvencaoEmpresa.convencao_id).filter(
        ConvencaoEmpresa.company_id.in_(company_ids)
    ).distinct().all()
    convencao_ids = [c[0] for c in convencao_ids]
    
    convencoes = db.query(Convencao).filter(
        Convencao.id.in_(convencao_ids)
    ).order_by(Convencao.data_publicacao.desc()).limit(limit).all()
    
    return convencoes

