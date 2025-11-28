"""
Celery task for checking dissidio alerts (convenção expiration warnings)
"""
from celery import Celery
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.config import settings
from app.models.convencao import Convencao, ConvencaoEmpresa
from app.models.company import Company
from app.models.notification import Notification
from datetime import date, timedelta
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

# Initialize Celery (reuse existing instance)
celery_app = Celery(
    "convencao_coletiva",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)


@celery_app.task(name="check_dissidio_alerts")
def check_dissidio_alerts_task():
    """
    Verifica convenções próximas do vencimento e gera alertas de dissídio
    Executa diariamente para verificar vencimentos
    """
    db = SessionLocal()
    hoje = date.today()
    
    try:
        logger.info("Iniciando verificação de alertas de dissídio...")
        
        # Buscar convenções ativas (vigência ainda válida)
        convencoes_ativas = db.query(Convencao).filter(
            Convencao.data_vigencia_fim >= hoje,
            Convencao.status == 'PROCESSADO'
        ).all()
        
        alertas_gerados = 0
        
        for convencao in convencoes_ativas:
            if not convencao.data_vigencia_fim:
                continue
                
            dias_restantes = (convencao.data_vigencia_fim - hoje).days
            
            # Definir tipo de alerta baseado em dias restantes
            tipo_alerta = None
            prioridade = None
            
            if dias_restantes <= 7:
                tipo_alerta = 'VENCIMENTO_URGENTE_7'
                prioridade = 'URGENTE'
            elif dias_restantes <= 15:
                tipo_alerta = 'VENCIMENTO_URGENTE_15'
                prioridade = 'URGENTE'
            elif dias_restantes <= 30:
                tipo_alerta = 'VENCIMENTO_PROXIMO_30'
                prioridade = 'ALTA'
            elif dias_restantes <= 60:
                tipo_alerta = 'VENCIMENTO_PROXIMO_60'
                prioridade = 'MEDIA'
            elif dias_restantes <= 90:
                tipo_alerta = 'VENCIMENTO_PROXIMO_90'
                prioridade = 'BAIXA'
            else:
                continue  # Ainda não precisa alertar
            
            # Gerar notificações para empresas afetadas
            count = generate_dissidio_alert(convencao, tipo_alerta, dias_restantes, prioridade, db)
            alertas_gerados += count
        
        # Verificar convenções vencidas sem renovação
        convencoes_vencidas = db.query(Convencao).filter(
            Convencao.data_vigencia_fim < hoje,
            Convencao.status == 'PROCESSADO'
        ).all()
        
        for convencao in convencoes_vencidas:
            # Verificar se já existe convenção nova para mesma empresa/CNAE
            if not has_new_negotiation(convencao, db):
                dias_vencido = (hoje - convencao.data_vigencia_fim).days
                # Alertar apenas se vencido há menos de 180 dias (6 meses)
                if dias_vencido <= 180:
                    count = generate_dissidio_alert(
                        convencao, 
                        'VENCIDO', 
                        -dias_vencido, 
                        'ALTA', 
                        db
                    )
                    alertas_gerados += count
        
        logger.info(f"Verificação concluída. {alertas_gerados} alertas gerados.")
        return {"status": "success", "alertas_gerados": alertas_gerados}
        
    except Exception as e:
        logger.error(f"Erro ao verificar alertas de dissídio: {e}")
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()


def generate_dissidio_alert(
    convencao: Convencao, 
    tipo_alerta: str, 
    dias_restantes: int,
    prioridade: str,
    db: Session
) -> int:
    """
    Gera alertas de dissídio para empresas afetadas por uma convenção
    
    Args:
        convencao: Convenção que está vencendo ou vencida
        tipo_alerta: Tipo do alerta (VENCIMENTO_PROXIMO_30, VENCIDO, etc.)
        dias_restantes: Dias restantes até vencimento (negativo se já vencido)
        prioridade: Prioridade do alerta (URGENTE, ALTA, MEDIA, BAIXA)
        db: Sessão do banco de dados
    
    Returns:
        Número de alertas gerados
    """
    # Buscar empresas associadas a esta convenção
    associations = db.query(ConvencaoEmpresa).filter(
        ConvencaoEmpresa.convencao_id == convencao.id
    ).all()
    
    if not associations:
        # Se não há associações diretas, buscar por CNAE e município
        companies = db.query(Company).filter(
            Company.cnae == convencao.cnae,
            Company.municipio == convencao.municipio,
            Company.uf == convencao.uf
        ).all()
        
        user_ids = {company.user_id for company in companies if company.user_id}
    else:
        # Obter user_ids das empresas associadas
        company_ids = [assoc.company_id for assoc in associations]
        companies = db.query(Company).filter(Company.id.in_(company_ids)).all()
        user_ids = {company.user_id for company in companies if company.user_id}
    
    if not user_ids:
        return 0
    
    alertas_gerados = 0
    
    # Criar mensagens personalizadas baseadas no tipo de alerta
    titulo, mensagem = get_alert_message(tipo_alerta, convencao, dias_restantes)
    
    for user_id in user_ids:
        # Verificar se já existe alerta similar não lido para evitar duplicatas
        existing = db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.convencao_id == convencao.id,
            Notification.tipo == tipo_alerta,
            Notification.lida == False
        ).first()
        
        if existing:
            # Atualizar mensagem se necessário
            if existing.mensagem != mensagem:
                existing.mensagem = mensagem
                existing.titulo = titulo
                db.commit()
            continue
        
        # Criar nova notificação
        notification = Notification(
            user_id=user_id,
            convencao_id=convencao.id,
            tipo=tipo_alerta,
            titulo=titulo,
            mensagem=mensagem
        )
        db.add(notification)
        alertas_gerados += 1
    
    db.commit()
    return alertas_gerados


def get_alert_message(tipo_alerta: str, convencao: Convencao, dias_restantes: int) -> Tuple[str, str]:
    """
    Gera título e mensagem para o alerta baseado no tipo
    
    Returns:
        Tuple (titulo, mensagem)
    """
    titulo_conv = convencao.titulo or 'Convenção Coletiva'
    data_vencimento = convencao.data_vigencia_fim.strftime('%d/%m/%Y') if convencao.data_vigencia_fim else 'N/A'
    
    if tipo_alerta.startswith('VENCIMENTO_URGENTE'):
        if '7' in tipo_alerta:
            titulo = f"⚠️ URGENTE: Convenção vence em 7 dias"
            mensagem = f"A convenção '{titulo_conv}' vence em {abs(dias_restantes)} dias ({data_vencimento}). É necessário iniciar a negociação para renovação."
        else:  # 15 dias
            titulo = f"⚠️ URGENTE: Convenção vence em 15 dias"
            mensagem = f"A convenção '{titulo_conv}' vence em {abs(dias_restantes)} dias ({data_vencimento}). Prepare-se para iniciar a negociação."
    
    elif tipo_alerta.startswith('VENCIMENTO_PROXIMO'):
        if '30' in tipo_alerta:
            titulo = f"🔔 Convenção vence em 30 dias"
            mensagem = f"A convenção '{titulo_conv}' vence em {dias_restantes} dias ({data_vencimento}). Considere iniciar o processo de renovação."
        elif '60' in tipo_alerta:
            titulo = f"📅 Convenção vence em 60 dias"
            mensagem = f"A convenção '{titulo_conv}' vence em {dias_restantes} dias ({data_vencimento}). Planeje a renovação."
        else:  # 90 dias
            titulo = f"📋 Convenção vence em 90 dias"
            mensagem = f"A convenção '{titulo_conv}' vence em {dias_restantes} dias ({data_vencimento}). Fique atento ao prazo de renovação."
    
    elif tipo_alerta == 'VENCIDO':
        titulo = f"❌ Convenção vencida"
        mensagem = f"A convenção '{titulo_conv}' venceu há {abs(dias_restantes)} dias ({data_vencimento}). Verifique se há nova negociação em andamento ou se é necessário renovar."
    
    else:
        titulo = f"Alerta de convenção"
        mensagem = f"A convenção '{titulo_conv}' requer atenção."
    
    return titulo, mensagem


def has_new_negotiation(convencao: Convencao, db: Session) -> bool:
    """
    Verifica se já existe uma convenção mais recente para o mesmo CNAE/município
    (indicando que já há uma nova negociação)
    
    Args:
        convencao: Convenção vencida a verificar
        db: Sessão do banco de dados
    
    Returns:
        True se existe nova negociação, False caso contrário
    """
    if not convencao.cnae or not convencao.municipio:
        return False
    
    # Buscar convenções mais recentes para mesmo CNAE/município
    novas_convencoes = db.query(Convencao).filter(
        Convencao.cnae == convencao.cnae,
        Convencao.municipio == convencao.municipio,
        Convencao.uf == convencao.uf,
        Convencao.data_publicacao > convencao.data_publicacao,
        Convencao.id != convencao.id,
        Convencao.status == 'PROCESSADO'
    ).count()
    
    return novas_convencoes > 0

