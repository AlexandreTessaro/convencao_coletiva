"""
API endpoint for manually triggering convenções collection
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.services.scraper import MediadorScraper
from app.services.document_processor import DocumentProcessor
from app.models.convencao import Convencao, ConvencaoEmpresa
from app.models.company import Company
from app.models.notification import Notification
from app.tasks.dissidio_alerts import check_dissidio_alerts_task
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


def associate_convencao_to_companies(convencao: Convencao, db: Session):
    """Associate convenção with relevant companies"""
    # Find companies by CNAE
    companies_cnae = []
    if convencao.cnae:
        companies_cnae = db.query(Company).filter(Company.cnae == convencao.cnae).all()
    
    # Find companies by municipio
    companies_municipio = []
    if convencao.municipio and convencao.uf:
        companies_municipio = db.query(Company).filter(
            Company.municipio == convencao.municipio,
            Company.uf == convencao.uf
        ).all()
    
    # Combine and remove duplicates
    all_companies = list(set(companies_cnae + companies_municipio))
    
    # Create associations
    for company in all_companies:
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
    """Calculate relevance score"""
    score = 0.0
    
    if convencao.cnae == company.cnae:
        score += 50.0
    
    if convencao.municipio == company.municipio and convencao.uf == company.uf:
        score += 50.0
    
    return score


def generate_notifications(convencao: Convencao, db: Session):
    """Generate notifications for relevant users"""
    # Get companies associated with this convenção
    associations = db.query(ConvencaoEmpresa).filter(
        ConvencaoEmpresa.convencao_id == convencao.id
    ).all()
    
    user_ids = set()
    for assoc in associations:
        company = db.query(Company).filter(Company.id == assoc.company_id).first()
        if company:
            user_ids.add(company.user_id)
    
    # Create notifications
    for user_id in user_ids:
        notification = Notification(
            user_id=user_id,
            convencao_id=convencao.id,
            tipo='NOVA_CONVENCAO',
            titulo=f"Nova convenção: {convencao.titulo or 'Sem título'}",
            mensagem=f"Uma nova convenção coletiva foi publicada e pode ser aplicável às suas empresas."
        )
        db.add(notification)
    
    db.commit()


@router.post("/collect", status_code=status.HTTP_202_ACCEPTED)
async def collect_convencoes(
    background_tasks: BackgroundTasks,
    limit: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Manually trigger collection of convenções from Mediador MTE
    
    Args:
        limit: Maximum number of convenções to collect (None = all)
        background_tasks: FastAPI background tasks
        current_user: Current authenticated user
        db: Database session
    """
    try:
        # Run collection in background
        background_tasks.add_task(
            run_collection_task,
            limit=limit,
            db=db
        )
        
        return {
            "status": "accepted",
            "message": "Coleta iniciada em background. Verifique os logs para acompanhar o progresso."
        }
    except Exception as e:
        logger.error(f"Error starting collection: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao iniciar coleta: {str(e)}"
        )


def run_collection_task(limit: Optional[int] = None, db: Session = None):
    """
    Run the collection task (can be called directly or as background task)
    """
    if db is None:
        from app.core.database import SessionLocal
        db = SessionLocal()
    
    scraper = MediadorScraper()
    processor = DocumentProcessor()
    
    try:
        logger.info("Starting convenções collection...")
        
        # Extract instrumento IDs
        logger.info("Extracting instrumento IDs...")
        instrumento_ids = scraper.extract_instrumento_ids()
        
        if limit:
            instrumento_ids = instrumento_ids[:limit]
        
        logger.info(f"Found {len(instrumento_ids)} instrumento IDs to process")
        
        new_count = 0
        error_count = 0
        
        for instrumento_id in instrumento_ids:
            try:
                # Check if already exists
                existing = db.query(Convencao).filter(
                    Convencao.instrumento_id == instrumento_id
                ).first()
                
                if existing:
                    logger.debug(f"Convenção {instrumento_id} already exists, skipping")
                    continue
                
                # Extract metadata
                logger.info(f"Extracting metadata for {instrumento_id}...")
                metadados = scraper.extract_metadados(instrumento_id)
                
                if not metadados:
                    logger.warning(f"No metadata extracted for {instrumento_id}")
                    error_count += 1
                    continue
                
                # Download documento (optional - can skip if URL not available)
                documento_path = None
                texto_extraido = None
                formato = None
                
                if metadados.get('documento_url'):
                    logger.info(f"Downloading documento for {instrumento_id}...")
                    download_result = scraper.download_documento(
                        metadados['documento_url'],
                        instrumento_id
                    )
                    
                    if download_result:
                        filepath, file_ext = download_result
                        
                        # Extract text
                        logger.info(f"Extracting text for {instrumento_id}...")
                        texto_extraido, formato = processor.extract_text(filepath, file_ext)
                        documento_path = filepath
                
                # Parse dates
                from datetime import datetime
                from dateutil import parser
                
                data_publicacao = None
                if metadados.get('data_publicacao'):
                    try:
                        data_publicacao = parser.parse(metadados['data_publicacao'], dayfirst=True).date()
                    except:
                        pass
                
                vigencia_inicio = None
                if metadados.get('vigencia_inicio'):
                    try:
                        vigencia_inicio = parser.parse(metadados['vigencia_inicio'], dayfirst=True).date()
                    except:
                        pass
                
                vigencia_fim = None
                if metadados.get('vigencia_fim'):
                    try:
                        vigencia_fim = parser.parse(metadados['vigencia_fim'], dayfirst=True).date()
                    except:
                        pass
                
                # Create convenção record
                convencao = Convencao(
                    instrumento_id=instrumento_id,
                    titulo=metadados.get('titulo') or f"Convenção {instrumento_id}",
                    tipo=metadados.get('tipo') or 'CCT',
                    data_publicacao=data_publicacao,
                    data_vigencia_inicio=vigencia_inicio,
                    data_vigencia_fim=vigencia_fim,
                    sindicato_empregador=metadados.get('sindicato_empregador'),
                    sindicato_trabalhador=metadados.get('sindicato_trabalhador'),
                    municipio=metadados.get('municipio'),
                    uf=metadados.get('uf'),
                    cnae=metadados.get('cnae'),
                    documento_url=metadados.get('documento_url'),
                    documento_path=documento_path,
                    texto_extraido=texto_extraido[:1000000] if texto_extraido else None,  # Limit to 1MB
                    formato_documento=formato,
                    status='PROCESSADO' if texto_extraido else 'PROCESSANDO'
                )
                
                db.add(convencao)
                db.commit()
                db.refresh(convencao)
                
                # Associate with companies
                associate_convencao_to_companies(convencao, db)
                
                # Generate notifications
                generate_notifications(convencao, db)
                
                new_count += 1
                logger.info(f"Successfully processed {instrumento_id}")
                
            except Exception as e:
                logger.error(f"Error processing {instrumento_id}: {e}")
                db.rollback()
                error_count += 1
                continue
        
        logger.info(f"Collection complete. {new_count} new convenções added, {error_count} errors")
        return {"status": "success", "new_count": new_count, "error_count": error_count}
        
    except Exception as e:
        logger.error(f"Error in collection task: {e}")
        return {"status": "error", "message": str(e)}
    
    finally:
        if db:
            db.close()


@router.post("/check-dissidio-alerts", status_code=status.HTTP_202_ACCEPTED)
async def check_dissidio_alerts(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Manually trigger check for dissidio alerts (convenção expiration warnings)
    
    This will check all active convenções and generate alerts for those
    approaching expiration (90, 60, 30, 15, 7 days) or already expired.
    """
    try:
        # Run check in background
        background_tasks.add_task(check_dissidio_alerts_task)
        
        return {
            "status": "accepted",
            "message": "Verificação de alertas de dissídio iniciada em background."
        }
    except Exception as e:
        logger.error(f"Error starting dissidio alerts check: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao iniciar verificação de alertas: {str(e)}"
        )

