"""Test script for collection"""
import os
import sys

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

print(f"Script directory: {script_dir}")
print(f"Python path: {sys.path[:3]}")

try:
    from app.core.database import SessionLocal
    print("✓ Database module imported successfully")
    
    from app.services.scraper import MediadorScraper
    print("✓ Scraper module imported successfully")
    
    # Test scraper initialization
    scraper = MediadorScraper()
    print(f"✓ Scraper initialized with base URL: {scraper.base_url}")
    
    # Try to extract instrumento IDs (this will test the connection)
    print("\nTentando extrair IDs de instrumentos...")
    print("(Isso pode demorar alguns segundos e pode falhar se o site não estiver acessível)")
    
    instrumento_ids = scraper.extract_instrumento_ids()
    
    if instrumento_ids:
        print(f"✓ Encontrados {len(instrumento_ids)} IDs de instrumentos")
        print(f"Primeiros 5 IDs: {instrumento_ids[:5]}")
    else:
        print("⚠ Nenhum ID encontrado. Isso pode ser normal se:")
        print("  - O site não estiver acessível")
        print("  - Os seletores CSS precisarem ser ajustados")
        print("  - O site tiver proteção contra scraping")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✅ Teste concluído!")

