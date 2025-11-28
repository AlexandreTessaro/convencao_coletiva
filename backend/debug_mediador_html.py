"""
Script para debugar e salvar o HTML retornado pelo Mediador MTE
"""
import sys
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.mediador_api import MediadorAPIClient

def debug_mediador():
    """Salva o HTML retornado para análise"""
    client = MediadorAPIClient()
    
    print("=" * 60)
    print("Debug: Salvando HTML do Mediador MTE")
    print("=" * 60)
    
    # Tentar diferentes URLs
    urls_to_test = [
        f"{client.base_url}/ConvencaoColetiva/Consulta",
        f"{client.base_url}/Consulta/ConvencaoColetiva",
        f"{client.base_url}/Consulta",
        f"{client.base_url}/InstrumentosColetivos/Consulta",
        f"{client.base_url}/busca",
        f"{client.base_url}/pesquisa",
        f"{client.base_url}/",
    ]
    
    os.makedirs('debug_html', exist_ok=True)
    
    for url in urls_to_test:
        try:
            print(f"\nTestando: {url}")
            response = client.session.get(url, timeout=30, allow_redirects=True)
            
            print(f"  Status: {response.status_code}")
            print(f"  URL final: {response.url}")
            print(f"  Tamanho: {len(response.content)} bytes")
            
            if response.status_code == 200:
                # Salvar HTML
                filename = url.split('/')[-1] or 'index'
                filename = filename.replace('?', '_').replace('=', '_')
                filepath = f"debug_html/{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                print(f"  ✓ HTML salvo em: {filepath}")
                
                # Analisar conteúdo
                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.find('title')
                if title:
                    print(f"  Título: {title.get_text()}")
                
                # Contar links
                links = soup.find_all('a', href=True)
                print(f"  Total de links: {len(links)}")
                
                # Procurar por links que parecem ser de convenções
                convencao_links = [l for l in links if any(kw in l.get('href', '').lower() for kw in ['instrumento', 'convencao', 'registro'])]
                print(f"  Links relacionados: {len(convencao_links)}")
                
                if convencao_links:
                    print("  Primeiros 5 links relacionados:")
                    for link in convencao_links[:5]:
                        print(f"    - {link.get('href')}: {link.get_text(strip=True)[:50]}")
                
                # Procurar por formulários
                forms = soup.find_all('form')
                print(f"  Formulários encontrados: {len(forms)}")
                
                # Procurar por tabelas
                tables = soup.find_all('table')
                print(f"  Tabelas encontradas: {len(tables)}")
                
        except Exception as e:
            print(f"  ✗ Erro: {e}")
    
    print("\n" + "=" * 60)
    print("Debug concluído! Verifique os arquivos em debug_html/")
    print("=" * 60)

if __name__ == "__main__":
    debug_mediador()

