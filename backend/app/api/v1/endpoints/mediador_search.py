"""
Endpoint para buscar convenções diretamente do Mediador MTE em tempo real
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.services.mediador_api import MediadorAPIClient
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/search-live")
async def search_convencoes_live(
    municipio: Optional[str] = Query(None),
    uf: Optional[str] = Query(None),
    cnae: Optional[str] = Query(None),
    cnpj: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
):
    """
    Busca convenções diretamente do Mediador MTE em tempo real
    (sem armazenar no banco de dados)
    
    Nota: O site do Mediador MTE pode requerer autenticação ou ter estrutura
    que muda frequentemente. Se não encontrar resultados, use a busca no banco local.
    """
    try:
        client = MediadorAPIClient()
        
        convencoes = client.search_convencoes(
            municipio=municipio,
            uf=uf,
            cnae=cnae,
            cnpj=cnpj,
            limit=limit
        )
        
        response_data = {
            "total": len(convencoes),
            "results": convencoes,
            "source": "mediador_mte_live"
        }
        
        # Se não encontrou resultados, adicionar mensagem informativa
        if len(convencoes) == 0:
            response_data["message"] = (
                "Nenhuma convenção encontrada na busca em tempo real. "
                "O site do Mediador MTE pode requerer autenticação ou ter estrutura diferente. "
                "Tente usar a busca no 'Banco Local' ou 'Híbrido'."
            )
            response_data["suggestion"] = "use_local_or_hybrid"
        
        return response_data
        
    except Exception as e:
        logger.error(f"Erro ao buscar convenções do Mediador MTE: {e}")
        # Retornar resposta vazia ao invés de erro 500 para não quebrar a interface
        return {
            "total": 0,
            "results": [],
            "source": "mediador_mte_live",
            "error": str(e),
            "message": f"Erro ao buscar no Mediador MTE: {str(e)}. Tente usar a busca no banco local."
        }


@router.get("/search-hybrid")
async def search_convencoes_hybrid(
    municipio: Optional[str] = Query(None),
    uf: Optional[str] = Query(None),
    cnae: Optional[str] = Query(None),
    cnpj: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    use_live: bool = Query(False, description="Se True, busca também no Mediador MTE em tempo real"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Busca híbrida: dados do banco + busca em tempo real no Mediador MTE
    """
    from app.models.convencao import Convencao
    from sqlalchemy import or_
    
    results = []
    
    # 1. Buscar no banco de dados local
    query = db.query(Convencao)
    
    if municipio:
        query = query.filter(Convencao.municipio.ilike(f"%{municipio}%"))
    if uf:
        query = query.filter(Convencao.uf == uf.upper())
    if cnae:
        query = query.filter(Convencao.cnae == cnae.replace('-', '').replace('/', '')[:7])
    if q:
        query = query.filter(
            or_(
                Convencao.titulo.ilike(f"%{q}%"),
                Convencao.sindicato_empregador.ilike(f"%{q}%"),
                Convencao.sindicato_trabalhador.ilike(f"%{q}%"),
            )
        )
    
    # Paginação
    offset = (page - 1) * page_size
    db_results = query.order_by(Convencao.data_publicacao.desc()).offset(offset).limit(page_size).all()
    
    # Converter para dict
    for conv in db_results:
        results.append({
            'id': str(conv.id),
            'instrumento_id': conv.instrumento_id,
            'titulo': conv.titulo,
            'tipo': conv.tipo,
            'data_publicacao': conv.data_publicacao.isoformat() if conv.data_publicacao else None,
            'municipio': conv.municipio,
            'uf': conv.uf,
            'cnae': conv.cnae,
            'sindicato_empregador': conv.sindicato_empregador,
            'sindicato_trabalhador': conv.sindicato_trabalhador,
            'fonte': 'banco_local'
        })
    
    # 2. Se solicitado, buscar também no Mediador MTE em tempo real
    if use_live:
        try:
            client = MediadorAPIClient()
            live_results = client.search_convencoes(
                municipio=municipio,
                uf=uf,
                cnae=cnae,
                cnpj=cnpj,
                limit=page_size
            )
            
            # Adicionar resultados ao final (evitar duplicatas por instrumento_id)
            existing_ids = {r.get('instrumento_id') for r in results}
            for live_conv in live_results:
                if live_conv.get('instrumento_id') not in existing_ids:
                    results.append(live_conv)
                    existing_ids.add(live_conv.get('instrumento_id'))
            
        except Exception as e:
            logger.warning(f"Erro ao buscar dados em tempo real: {e}")
            # Continuar mesmo se a busca em tempo real falhar
    
    return {
        "total": len(results),
        "page": page,
        "page_size": page_size,
        "results": results[:page_size],  # Limitar ao tamanho da página
        "has_more": len(results) > page_size
    }

