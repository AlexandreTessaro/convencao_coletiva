"""
Celery task for collecting convenções
"""
from celery import Celery
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.config import settings
from app.models.convencao import Convencao
from app.models.company import Company
from app.models.convencao import ConvencaoEmpresa
from app.models.notification import Notification
from app.services.scraper import MediadorScraper
from app.services.document_processor import DocumentProcessor
import os
import logging

logger = logging.getLogger(__name__)

# Initialize Celery
celery_app = Celery(
    "convencao_coletiva",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)


@celery_app.task(name="collect_convencoes")
def collect_convencoes_task():
    """
    Main task to collect convenções from Mediador MTE
    """
    db = SessionLocal()
    scraper = MediadorScraper()
    processor = DocumentProcessor()
    
    try:
        # Extract instrumento IDs
        logger.info("Extracting instrumento IDs...")
        instrumento_ids = scraper.extract_instrumento_ids()
        logger.info(f"Found {len(instrumento_ids)} instrumento IDs")
        
        new_count = 0
        
        for instrumento_id in instrumento_ids:
            try:
                # Check if already exists
                existing = db.query(Convencao).filter(
                    Convencao.instrumento_id == instrumento_id
                ).first()
                
                if existing:
                    logger.info(f"Convenção {instrumento_id} already exists, skipping")
                    continue
                
                # Extract metadata
                logger.info(f"Extracting metadata for {instrumento_id}...")
                metadados = scraper.extract_metadados(instrumento_id)
                
                if not metadados or not metadados.get('documento_url'):
                    logger.warning(f"No metadata or document URL for {instrumento_id}")
                    continue
                
                # Download documento
                logger.info(f"Downloading documento for {instrumento_id}...")
                download_result = scraper.download_documento(
                    metadados['documento_url'],
                    instrumento_id
                )
                
                if not download_result:
                    logger.warning(f"Failed to download documento for {instrumento_id}")
                    continue
                
                filepath, file_ext = download_result
                
                # Extract text
                logger.info(f"Extracting text for {instrumento_id}...")
                texto_extraido, formato = processor.extract_text(filepath, file_ext)
                
                # Create convenção record
                convencao = Convencao(
                    instrumento_id=instrumento_id,
                    titulo=metadados.get('titulo'),
                    tipo='CCT',  # Default, can be improved
                    data_publicacao=metadados.get('data_publicacao'),
                    data_vigencia_inicio=metadados.get('vigencia_inicio'),
                    data_vigencia_fim=metadados.get('vigencia_fim'),
                    sindicato_empregador=metadados.get('sindicato_empregador'),
                    sindicato_trabalhador=metadados.get('sindicato_trabalhador'),
                    municipio=metadados.get('municipio'),
                    uf=metadados.get('uf'),
                    cnae=metadados.get('cnae'),
                    documento_url=metadados.get('documento_url'),
                    documento_path=filepath,
                    texto_extraido=texto_extraido[:1000000] if texto_extraido else None,  # Limit to 1MB
                    formato_documento=formato,
                    status='PROCESSADO' if texto_extraido else 'ERRO'
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
                
                # Clean up temp file (or move to permanent storage)
                # os.remove(filepath)  # Uncomment if using temp storage
                
            except Exception as e:
                logger.error(f"Error processing {instrumento_id}: {e}")
                db.rollback()
                continue
        
        logger.info(f"Collection complete. {new_count} new convenções added.")
        return {"status": "success", "new_count": new_count}
        
    except Exception as e:
        logger.error(f"Error in collection task: {e}")
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()


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

