from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.v1.api import api_router
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ConvençãoColetiva API",
    description="API para gestão de Convenções Coletivas de Trabalho",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS - Allow all origins in development
# Note: Cannot use ["*"] with allow_credentials=True
cors_origins = [
    "http://localhost:3000",
    "http://localhost:3001", 
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api/v1")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={
            "detail": f"Erro interno do servidor: {str(exc)}",
            "type": type(exc).__name__
        }
    )


@app.get("/")
async def root():
    return {
        "message": "ConvençãoColetiva API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
