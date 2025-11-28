"""
Script para executar coleta de convenções manualmente
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.api.v1.endpoints.collector import run_collection_task
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main function to run collection"""
    limit = None
    
    # Check for limit argument
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
            print(f"Limitando coleta a {limit} convenções")
        except ValueError:
            print("Uso: python collect_convencoes.py [limit]")
            print("Exemplo: python collect_convencoes.py 10")
            return
    
    print("=" * 60)
    print("Iniciando coleta de convenções do Mediador MTE")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        result = run_collection_task(limit=limit, db=db)
        
        print("\n" + "=" * 60)
        print("Coleta concluída!")
        print("=" * 60)
        print(f"Status: {result.get('status')}")
        if 'new_count' in result:
            print(f"Novas convenções adicionadas: {result['new_count']}")
        if 'error_count' in result:
            print(f"Erros: {result['error_count']}")
        if 'message' in result:
            print(f"Mensagem: {result['message']}")
        
    except Exception as e:
        logger.error(f"Erro ao executar coleta: {e}")
        print(f"\n❌ Erro: {e}")
        return 1
    
    finally:
        db.close()
    
    return 0


if __name__ == "__main__":
    exit(main())

