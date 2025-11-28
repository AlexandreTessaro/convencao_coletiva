"""
Script para criar dados de teste para o usuário atual logado
Execute: python create_test_data_for_current_user.py <email_do_usuario>
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.models.company import Company
from app.models.convencao import Convencao, ConvencaoEmpresa
from datetime import date

def create_test_data_for_user(user_email: str):
    db = SessionLocal()
    
    try:
        # Buscar usuário
        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            print(f"❌ Usuário {user_email} não encontrado!")
            print("Por favor, crie o usuário primeiro através do registro.")
            return
        
        print(f"✓ Usuário encontrado: {user.email} ({user.full_name})")
        
        # Criar empresa de teste para este usuário
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
        
        # Criar convenções de teste
        convencoes_data = [
            {
                "instrumento_id": f"TEST001-{str(user.id)[:8]}",
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
                "texto_extraido": "Convenção Coletiva de Trabalho. Salário mínimo. Vale transporte. Vale alimentação. Trabalhador. Benefícios. FGTS.",
                "status": "PROCESSADO"
            },
            {
                "instrumento_id": f"TEST002-{str(user.id)[:8]}",
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
                "instrumento_id": f"TEST003-{str(user.id)[:8]}",
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
                
                # Associar com a empresa
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
            print("✓ Convenções já existem para este usuário")
        else:
            print(f"✓ {created_count} convenção(ões) criada(s)")
        
        print("\n✅ Dados de teste criados com sucesso!")
        print(f"\nAgora você pode buscar convenções usando:")
        print(f"  - Município: São Paulo")
        print(f"  - UF: SP")
        print(f"  - CNAE: 4711-3/01")
        print(f"  - Palavra-chave: trabalhador, salário, vale transporte, FGTS")
        
    except Exception as e:
        print(f"❌ Erro ao criar dados de teste: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_email = sys.argv[1]
        create_test_data_for_user(user_email)
    else:
        print("Uso: python create_test_data_for_current_user.py <email_do_usuario>")
        print("Exemplo: python create_test_data_for_current_user.py teste@exemplo.com")



