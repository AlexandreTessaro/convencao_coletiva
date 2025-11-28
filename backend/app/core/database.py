from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

try:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        echo=False  # Set to True for SQL debugging
    )
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    Base = declarative_base()
    
    logger.info("Database engine created successfully")
except Exception as e:
    logger.error(f"Error creating database engine: {e}")
    raise


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

