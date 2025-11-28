"""
Script de debug para testar o scraper e ver o que está acontecendo
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.scraper import MediadorScraper
from app.core.config import settings
import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_scraper():
    """Test scraper with detailed output"""
    print("=" * 60)
    print("DEBUG: Testando Scraper do Mediador MTE")
    print("=" * 60)
    
    scraper = MediadorScraper()
    
    print(f"\n✓ Scraper inicializado")
    print(f"  Base URL: {scraper.base_url}")
    print(f"  User Agent: {scraper.user_agent}")
    print(f"  Delay: {scraper.delay}s")
    
    # Test 1: Verificar se o site está acessível
    print("\n" + "=" * 60)
    print("TESTE 1: Verificando acessibilidade do site")
    print("=" * 60)
    
    try:
        response = scraper.session.get(scraper.base_url, timeout=10)
        print(f"✓ Status Code: {response.status_code}")
        print(f"✓ URL final: {response.url}")
        print(f"✓ Tamanho da resposta: {len(response.content)} bytes")
        
        if response.status_code == 200:
            print("✓ Site está acessível!")
            
            # Verificar se é HTML
            if 'text/html' in response.headers.get('content-type', ''):
                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.find('title')
                if title:
                    print(f"✓ Título da página: {title.get_text()}")
                
                # Procurar por links relacionados a instrumentos
                links = soup.find_all('a', href=True)
                instrumento_links = [link for link in links if 'instrumento' in link.get('href', '').lower()]
                
                print(f"\n✓ Total de links encontrados: {len(links)}")
                print(f"✓ Links com 'instrumento': {len(instrumento_links)}")
                
                if instrumento_links:
                    print("\nPrimeiros 5 links encontrados:")
                    for i, link in enumerate(instrumento_links[:5], 1):
                        print(f"  {i}. {link.get('href')}")
        else:
            print(f"⚠ Site retornou status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro ao acessar site: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test 2: Tentar encontrar página de busca
    print("\n" + "=" * 60)
    print("TESTE 2: Tentando encontrar página de busca")
    print("=" * 60)
    
    search_urls = [
        f"{scraper.base_url}/busca",
        f"{scraper.base_url}/pesquisa",
        f"{scraper.base_url}/instrumentos",
        f"{scraper.base_url}/convencoes",
        f"{scraper.base_url}/",
    ]
    
    for url in search_urls:
        try:
            print(f"\nTentando: {url}")
            response = scraper.session.get(url, timeout=10)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Procurar por links de instrumentos
                links = soup.find_all('a', href=True)
                instrumento_links = [link.get('href') for link in links if 'instrumento' in link.get('href', '').lower()]
                
                if instrumento_links:
                    print(f"  ✓ Encontrados {len(instrumento_links)} links com 'instrumento'")
                    print(f"  Primeiros 3: {instrumento_links[:3]}")
                else:
                    print(f"  ⚠ Nenhum link com 'instrumento' encontrado")
                    
                # Procurar por formulários de busca
                forms = soup.find_all('form')
                if forms:
                    print(f"  ✓ Encontrados {len(forms)} formulários")
                
                # Procurar por campos de input
                inputs = soup.find_all('input')
                search_inputs = [inp for inp in inputs if inp.get('type') in ['text', 'search']]
                if search_inputs:
                    print(f"  ✓ Encontrados {len(search_inputs)} campos de busca")
        except Exception as e:
            print(f"  ❌ Erro: {e}")
    
    # Test 3: Tentar extrair IDs
    print("\n" + "=" * 60)
    print("TESTE 3: Tentando extrair IDs de instrumentos")
    print("=" * 60)
    
    try:
        instrumento_ids = scraper.extract_instrumento_ids()
        print(f"\n✓ IDs encontrados: {len(instrumento_ids)}")
        if instrumento_ids:
            print(f"Primeiros 5 IDs: {instrumento_ids[:5]}")
        else:
            print("⚠ Nenhum ID encontrado")
            print("\nPossíveis razões:")
            print("  1. O site pode ter estrutura diferente")
            print("  2. Pode precisar de autenticação")
            print("  3. Os seletores CSS podem estar incorretos")
            print("  4. O site pode ter proteção contra scraping")
            print("\nPróximos passos:")
            print("  1. Acesse manualmente: https://mediador.trabalho.gov.br")
            print("  2. Verifique a estrutura HTML da página")
            print("  3. Ajuste os seletores em backend/app/services/scraper.py")
    except Exception as e:
        print(f"❌ Erro ao extrair IDs: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("DEBUG concluído!")
    print("=" * 60)

if __name__ == "__main__":
    test_scraper()

