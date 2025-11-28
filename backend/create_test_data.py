"""
Script para criar dados de teste no banco de dados
Execute: python create_test_data.py
"""
import sys
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.user import User
from app.models.company import Company
from app.models.convencao import Convencao, ConvencaoEmpresa
from app.core.security import get_password_hash
from datetime import date, datetime
import uuid

def create_test_data(user_email: str = None):
    """
    Cria dados de teste no banco de dados
    Args:
        user_email: Email do usuário para associar os dados. Se None, usa teste@exemplo.com
    """
    db = SessionLocal()
    
    try:
        # 1. Criar ou buscar usuário
        if user_email:
            user = db.query(User).filter(User.email == user_email).first()
            if not user:
                print(f"❌ Usuário {user_email} não encontrado!")
                print("Por favor, crie o usuário primeiro através do registro.")
                return
        else:
            user = db.query(User).filter(User.email == "teste@exemplo.com").first()
        if not user:
            print("Criando usuário de teste...")
            user = User(
                email="teste@exemplo.com",
                hashed_password=get_password_hash("123456789"),
                full_name="Usuário Teste",
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"✓ Usuário criado: {user.email}")
        else:
            print(f"✓ Usuário já existe: {user.email}")
        
        # 2. Criar empresa de teste
        company = db.query(Company).filter(
            Company.user_id == user.id,
            Company.cnpj == "11222333000144"
        ).first()
        
        if not company:
            print("Criando empresa de teste...")
            company = Company(
                user_id=user.id,
                cnpj="11222333000144",
                razao_social="Empresa Teste LTDA",
                cnae="4711-3/01",
                municipio="São Paulo",
                uf="SP"
            )
            db.add(company)
            db.commit()
            db.refresh(company)
            print(f"✓ Empresa criada: {company.razao_social}")
        else:
            print(f"✓ Empresa já existe: {company.razao_social}")
        
        # 3. Criar convenções de teste
        convencoes_data = [
            {
                "instrumento_id": "TEST001",
                "titulo": "Convenção Coletiva de Trabalho - Comércio Varejista - São Paulo",
                "tipo": "CCT",
                "data_publicacao": date(2024, 1, 15),
                "data_vigencia_inicio": date(2024, 1, 1),
                "data_vigencia_fim": date(2024, 12, 31),
                "sindicato_empregador": "Sindicato do Comércio Varejista de São Paulo",
                "sindicato_trabalhador": "Sindicato dos Trabalhadores no Comércio de São Paulo",
                "municipio": "São Paulo",
                "uf": "SP",
                "cnae": "4711-3/01",
                "texto_extraido": "Convenção Coletiva de Trabalho. Salário mínimo. Vale transporte. Vale alimentação. Trabalhador. Benefícios.",
                "status": "PROCESSADO"
            },
            {
                "instrumento_id": "TEST002",
                "titulo": "Convenção Coletiva de Trabalho - Restaurantes - São Paulo",
                "tipo": "CCT",
                "data_publicacao": date(2024, 2, 1),
                "data_vigencia_inicio": date(2024, 2, 1),
                "data_vigencia_fim": date(2025, 1, 31),
                "sindicato_empregador": "Sindicato de Restaurantes de São Paulo",
                "sindicato_trabalhador": "Sindicato dos Trabalhadores em Restaurantes de São Paulo",
                "municipio": "São Paulo",
                "uf": "SP",
                "cnae": "5611-2/01",
                "texto_extraido": "Convenção Coletiva de Trabalho. Salário. Horário de trabalho. Férias. 13º salário. Vale transporte.",
                "status": "PROCESSADO"
            },
            {
                "instrumento_id": "TEST003",
                "titulo": "Convenção Coletiva de Trabalho - Tecnologia - São Paulo",
                "tipo": "CCT",
                "data_publicacao": date(2024, 3, 1),
                "data_vigencia_inicio": date(2024, 3, 1),
                "data_vigencia_fim": date(2025, 2, 28),
                "sindicato_empregador": "Sindicato das Empresas de Tecnologia de São Paulo",
                "sindicato_trabalhador": "Sindicato dos Trabalhadores em Tecnologia de São Paulo",
                "municipio": "São Paulo",
                "uf": "SP",
                "cnae": "6201-5/00",
                "texto_extraido": "Convenção Coletiva de Trabalho. Desenvolvimento de software. Trabalhador. Salário. Benefícios. Vale refeição.",
                "status": "PROCESSADO"
            }
        ]
        
        created_count = 0
        for conv_data in convencoes_data:
            existing = db.query(Convencao).filter(
                Convencao.instrumento_id == conv_data["instrumento_id"]
            ).first()
            
            if not existing:
                convencao = Convencao(**conv_data)
                db.add(convencao)
                db.commit()
                db.refresh(convencao)
                
                # Associar com a empresa se o CNAE corresponder
                if convencao.cnae == company.cnae or convencao.municipio == company.municipio:
                    association = ConvencaoEmpresa(
                        convencao_id=convencao.id,
                        company_id=company.id,
                        relevancia_score=100.0
                    )
                    db.add(association)
                    db.commit()
                
                created_count += 1
                print(f"✓ Convenção criada: {convencao.titulo}")
        
        if created_count == 0:
            print("✓ Convenções já existem")
        else:
            print(f"✓ {created_count} convenção(ões) criada(s)")
        
        print("\n✅ Dados de teste criados com sucesso!")
        print(f"\nVocê pode fazer login com:")
        print(f"  Email: teste@exemplo.com")
        print(f"  Senha: 123456789")
        print(f"\nE buscar convenções usando:")
        print(f"  - Município: São Paulo")
        print(f"  - UF: SP")
        print(f"  - CNAE: 4711-3/01")
        print(f"  - Palavra-chave: trabalhador, salário, vale transporte")
        
    except Exception as e:
        print(f"❌ Erro ao criar dados de teste: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()

