from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.user import User
from app.models.notification import Notification, NotificationPreference
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.notification import NotificationResponse, NotificationPreferenceUpdate

router = APIRouter()


@router.get("", response_model=List[NotificationResponse])
async def list_notifications(
    lida: bool = None,
    tipo: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List notifications for current user"""
    query = db.query(Notification).filter(Notification.user_id == current_user.id)
    
    if lida is not None:
        query = query.filter(Notification.lida == lida)
    
    if tipo:
        query = query.filter(Notification.tipo == tipo)
    
    notifications = query.order_by(Notification.created_at.desc()).limit(50).all()
    return notifications


@router.get("/dissidio", response_model=List[NotificationResponse])
async def list_dissidio_alerts(
    lida: bool = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List dissidio alerts (vencimento de convenções) for current user"""
    # Tipos de alerta de dissídio
    dissidio_types = [
        'VENCIMENTO_PROXIMO_90',
        'VENCIMENTO_PROXIMO_60',
        'VENCIMENTO_PROXIMO_30',
        'VENCIMENTO_URGENTE_15',
        'VENCIMENTO_URGENTE_7',
        'VENCIDO'
    ]
    
    query = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.tipo.in_(dissidio_types)
    )
    
    if lida is not None:
        query = query.filter(Notification.lida == lida)
    
    notifications = query.order_by(Notification.created_at.desc()).limit(50).all()
    return notifications


@router.put("/{notification_id}/read", response_model=NotificationResponse)
async def mark_as_read(
    notification_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark notification as read"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notificação não encontrada")
    
    notification.lida = True
    db.commit()
    db.refresh(notification)
    
    return notification


@router.get("/preferences", response_model=NotificationPreferenceUpdate)
async def get_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get notification preferences"""
    prefs = db.query(NotificationPreference).filter(
        NotificationPreference.user_id == current_user.id
    ).first()
    
    if not prefs:
        # Create default preferences
        prefs = NotificationPreference(
            user_id=current_user.id
        )
        db.add(prefs)
        db.commit()
        db.refresh(prefs)
    
    return prefs


@router.put("/preferences", response_model=NotificationPreferenceUpdate)
async def update_preferences(
    preferences: NotificationPreferenceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update notification preferences"""
    prefs = db.query(NotificationPreference).filter(
        NotificationPreference.user_id == current_user.id
    ).first()
    
    if not prefs:
        prefs = NotificationPreference(user_id=current_user.id)
        db.add(prefs)
    
    for key, value in preferences.dict(exclude_unset=True).items():
        setattr(prefs, key, value)
    
    db.commit()
    db.refresh(prefs)
    
    return prefs

