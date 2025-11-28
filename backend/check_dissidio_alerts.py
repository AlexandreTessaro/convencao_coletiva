"""
Script para executar manualmente a verificação de alertas de dissídio
"""
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.tasks.dissidio_alerts import check_dissidio_alerts_task

if __name__ == "__main__":
    print("Iniciando verificação de alertas de dissídio...")
    result = check_dissidio_alerts_task()
    print(f"\nResultado: {result}")
    if result.get("status") == "success":
        print(f"✅ {result.get('alertas_gerados', 0)} alertas gerados com sucesso!")
    else:
        print(f"❌ Erro: {result.get('message', 'Erro desconhecido')}")

