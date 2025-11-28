"""
Script de coleta com fallback para dados de teste se o scraper não encontrar dados
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.api.v1.endpoints.collector import run_collection_task
from app.models.convencao import Convencao
from app.models.company import Company
from app.models.convencao import ConvencaoEmpresa
from datetime import date
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def create_sample_data(db, limit=5):
    """Create sample convenções data for testing"""
    print(f"\nCriando {limit} convenções de exemplo...")
    
    # Check if user has companies
    companies = db.query(Company).all()
    
    if not companies:
        print("⚠️  Nenhuma empresa cadastrada. Criando empresa de exemplo...")
        from app.models.user import User
        user = db.query(User).first()
        if not user:
            print("❌ Nenhum usuário encontrado. Crie um usuário primeiro.")
            return 0
        
        company = Company(
            user_id=user.id,
            razao_social="Empresa Exemplo Ltda",
            cnpj="12345678000190",
            cnae="62015",  # Formato curto (sem hífen e barra)
            municipio="São Paulo",
            uf="SP"
        )
        db.add(company)
        db.commit()
        companies = [company]
    
    created = 0
    for i in range(limit):
        instrumento_id = f"SAMPLE-{i+1:03d}"
        
        # Check if already exists
        existing = db.query(Convencao).filter(
            Convencao.instrumento_id == instrumento_id
        ).first()
        
        if existing:
            continue
        
        convencao = Convencao(
            instrumento_id=instrumento_id,
            titulo=f"Convenção Coletiva de Trabalho - Exemplo {i+1}",
            tipo="CCT",
            data_publicacao=date(2024, 1, 1 + i),
            data_vigencia_inicio=date(2024, 1, 1 + i),
            data_vigencia_fim=date(2025, 12, 31),
            sindicato_empregador=f"Sindicato Empregador Exemplo {i+1}",
            sindicato_trabalhador=f"Sindicato Trabalhador Exemplo {i+1}",
            municipio=["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Curitiba", "Porto Alegre"][i % 5],
            uf=["SP", "RJ", "MG", "PR", "RS"][i % 5],
            cnae=["62015", "62023", "62031", "62040", "62091"][i % 5],  # Formato curto (máx 7 caracteres)
            texto_extraido=f"Texto exemplo da convenção {i+1}. Esta é uma convenção coletiva de trabalho de exemplo.",
            status="PROCESSADO"
        )
        
        db.add(convencao)
        db.commit()
        db.refresh(convencao)
        
        # Associate with first company
        if companies:
            association = ConvencaoEmpresa(
                convencao_id=convencao.id,
                company_id=companies[0].id,
                relevancia_score=100.0
            )
            db.add(association)
            db.commit()
        
        created += 1
        print(f"  ✓ Criada: {convencao.titulo}")
    
    return created


def main():
    """Main function"""
    limit = None
    
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
        except ValueError:
            print("Uso: python collect_with_fallback.py [limit]")
            return 1
    
    print("=" * 60)
    print("Coleta de Convenções (com fallback para dados de teste)")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # Try real collection first
        print("\n1. Tentando coleta real do Mediador MTE...")
        result = run_collection_task(limit=limit, db=db)
        
        new_count = result.get('new_count', 0)
        
        if new_count == 0:
            print("\n⚠️  Nenhuma convenção encontrada na coleta real.")
            
            # Ask if should create sample data
            print("\n2. Criando dados de exemplo para teste...")
            sample_count = create_sample_data(db, limit=limit or 5)
            
            if sample_count > 0:
                print(f"\n✓ {sample_count} convenções de exemplo criadas!")
                print("\nAgora você pode:")
                print("  - Testar a busca de convenções")
                print("  - Verificar a interface")
                print("  - Ajustar o scraper para funcionar com o site real")
            else:
                print("⚠️  Nenhuma convenção de exemplo criada (já existem?)")
        else:
            print(f"\n✓ {new_count} convenções coletadas do site real!")
        
        # Show total count
        total = db.query(Convencao).count()
        print(f"\nTotal de convenções no banco: {total}")
        
    except Exception as e:
        logger.error(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    finally:
        db.close()
    
    return 0


if __name__ == "__main__":
    exit(main())

