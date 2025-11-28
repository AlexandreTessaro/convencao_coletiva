from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS - Parse from comma-separated string or JSON array
    CORS_ORIGINS: str = "http://localhost:3000"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS from string to list"""
        if not self.CORS_ORIGINS:
            return ["http://localhost:3000"]
        # Try JSON first
        try:
            return json.loads(self.CORS_ORIGINS)
        except json.JSONDecodeError:
            # Fallback to comma-separated string
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Email (configure via environment variables, never hardcode credentials)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""  # Set via .env file
    SMTP_PASSWORD: str = ""  # Set via .env file
    SMTP_FROM: str = "noreply@convencaocoletiva.com.br"
    
    # Storage
    STORAGE_TYPE: str = "local"
    STORAGE_PATH: str = "./storage"
    
    # Scraper
    SCRAPER_DELAY_SECONDS: int = 3
    SCRAPER_USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    MEDIADOR_BASE_URL: str = "https://mediador.trabalho.gov.br"
    MEDIADOR_API_URL: str = "https://www3.mte.gov.br/sistemas/mediador"
    
    # OCR
    TESSERACT_CMD: str = "/usr/bin/tesseract"
    OCR_LANG: str = "por"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

