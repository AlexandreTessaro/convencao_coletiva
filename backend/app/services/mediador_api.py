"""
Serviço para buscar dados do Mediador MTE em tempo real
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from app.core.config import settings
import logging
import re
from datetime import datetime
from dateutil import parser

logger = logging.getLogger(__name__)


class MediadorAPIClient:
    """Cliente para buscar dados do Mediador MTE"""
    
    def __init__(self):
        # URL real do Mediador MTE - tentar diferentes padrões
        self.base_urls = [
            "https://www3.mte.gov.br/sistemas/mediador",
            "https://mediador.trabalho.gov.br",
            "http://mediador.mte.gov.br",
        ]
        self.base_url = self.base_urls[0]  # Usar o primeiro como padrão
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': 'https://www3.mte.gov.br/',
        })
    
    def search_convencoes(
        self,
        municipio: Optional[str] = None,
        uf: Optional[str] = None,
        cnae: Optional[str] = None,
        cnpj: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict]:
        """
        Busca convenções no Mediador MTE
        
        Args:
            municipio: Nome do município
            uf: Sigla do estado (ex: SP, RJ)
            cnae: Código CNAE
            cnpj: CNPJ da empresa
            limit: Limite de resultados
            
        Returns:
            Lista de convenções encontradas
        """
        convencoes = []
        
        try:
            # Tentar diferentes URLs de busca
            search_urls = [
                f"{self.base_url}/ConvencaoColetiva/Consulta",
                f"{self.base_url}/Consulta/ConvencaoColetiva",
                f"{self.base_url}/Consulta",
                f"{self.base_url}/InstrumentosColetivos/Consulta",
                f"{self.base_url}/busca",
                f"{self.base_url}/pesquisa",
                f"{self.base_url}/",
            ]
            
            # Preparar parâmetros de busca
            params = {}
            if municipio:
                params['municipio'] = municipio
            if uf:
                params['uf'] = uf.upper()
            if cnae:
                # Remover formatação do CNAE
                cnae_clean = cnae.replace('-', '').replace('/', '')
                params['cnae'] = cnae_clean
            if cnpj:
                # Remover formatação do CNPJ
                cnpj_clean = cnpj.replace('.', '').replace('/', '').replace('-', '')
                params['cnpj'] = cnpj_clean
            
            response = None
            soup = None
            
            # Tentar cada URL até encontrar uma que funcione
            for search_url in search_urls:
                try:
                    logger.info(f"Tentando buscar em: {search_url} com parâmetros: {params}")
                    response = self.session.get(search_url, params=params, timeout=30, allow_redirects=True)
                    
                    # Garantir encoding UTF-8
                    if response.encoding is None or response.encoding.lower() not in ['utf-8', 'utf8']:
                        response.encoding = 'utf-8'
                    
                    # Verificar se a resposta é válida
                    if response.status_code == 200:
                        # Verificar se a página contém conteúdo relevante
                        content_lower = response.text.lower()
                        
                        # Verificar se tem resultados de busca (tabelas com dados, listas de resultados, etc.)
                        # Usar encoding UTF-8 explicitamente
                        temp_soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
                        has_results = (
                            len(temp_soup.find_all('table')) > 0 or
                            len(temp_soup.find_all(['div', 'ul'], class_=re.compile(r'result|lista|tabela', re.I))) > 0 or
                            len([l for l in temp_soup.find_all('a', href=True) if re.search(r'/\d{6,}', l.get('href', ''))]) > 0
                        )
                        
                        # Verificar se tem conteúdo relevante (mesmo que seja página inicial, pode ter links úteis)
                        has_relevant_content = any(keyword in content_lower for keyword in ['convenção', 'instrumento', 'coletivo', 'trabalho'])
                        
                        # Aceitar se tem resultados OU se tem conteúdo relevante (vamos filtrar depois)
                        if has_results or has_relevant_content:
                            soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
                            logger.info(f"✓ URL funcionando: {search_url}")
                            break
                        else:
                            logger.debug(f"Página não contém conteúdo relevante: {search_url}")
                    elif response.status_code in [301, 302, 303, 307, 308]:
                        # Seguir redirect
                        redirect_url = response.headers.get('Location', '')
                        if redirect_url:
                            if not redirect_url.startswith('http'):
                                redirect_url = f"{self.base_url}{redirect_url}"
                            logger.info(f"Redirect detectado para: {redirect_url}")
                            response = self.session.get(redirect_url, timeout=30)
                            if response.encoding is None or response.encoding.lower() not in ['utf-8', 'utf8']:
                                response.encoding = 'utf-8'
                            if response.status_code == 200:
                                soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
                                logger.info(f"✓ URL após redirect funcionando: {redirect_url}")
                                break
                except requests.RequestException as e:
                    logger.debug(f"Erro ao acessar {search_url}: {e}")
                    continue
            
            if not soup:
                logger.warning("Nenhuma URL de busca funcionou. Tentando navegar pela página inicial...")
                # Tentar acessar a página inicial e procurar por links de consulta
                try:
                    home_response = self.session.get(self.base_url, timeout=10)
                    if home_response.encoding is None or home_response.encoding.lower() not in ['utf-8', 'utf8']:
                        home_response.encoding = 'utf-8'
                    if home_response.status_code == 200:
                        home_soup = BeautifulSoup(home_response.content, 'html.parser', from_encoding='utf-8')
                        
                        # Procurar por links que levem à área de consulta
                        consulta_keywords = ['consultar', 'consulta', 'instrumentos coletivos', 'registrados']
                        consulta_links = []
                        
                        for link in home_soup.find_all('a', href=True):
                            href = link.get('href', '').lower()
                            text = link.get_text(strip=True).lower()
                            
                            if any(kw in href or kw in text for kw in consulta_keywords):
                                full_url = href if href.startswith('http') else f"{self.base_url}{href}"
                                consulta_links.append(full_url)
                        
                        # Tentar acessar os links de consulta encontrados
                        for consulta_url in consulta_links[:3]:  # Tentar até 3 links
                            try:
                                logger.info(f"Tentando link de consulta encontrado: {consulta_url}")
                                consulta_response = self.session.get(consulta_url, params=params, timeout=30)
                                if consulta_response.encoding is None or consulta_response.encoding.lower() not in ['utf-8', 'utf8']:
                                    consulta_response.encoding = 'utf-8'
                                if consulta_response.status_code == 200:
                                    consulta_soup = BeautifulSoup(consulta_response.content, 'html.parser', from_encoding='utf-8')
                                    # Verificar se tem resultados
                                    if len(consulta_soup.find_all('table')) > 0 or len([l for l in consulta_soup.find_all('a', href=True) if re.search(r'/\d{6,}', l.get('href', ''))]) > 0:
                                        soup = consulta_soup
                                        logger.info(f"✓ Encontrada página de consulta: {consulta_url}")
                                        break
                            except:
                                continue
                        
                        if not soup:
                            logger.info("Página inicial acessível, mas não foi possível encontrar área de consulta pública.")
                except:
                    logger.warning("Não foi possível acessar nem a página inicial.")
                
                if not soup:
                    return []
            
            # Extrair convenções da página
            convencoes = self._parse_search_results(soup, limit)
            
            logger.info(f"Encontradas {len(convencoes)} convenções")
            
        except requests.RequestException as e:
            logger.error(f"Erro ao buscar convenções: {e}")
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar convenções: {e}")
            import traceback
            logger.error(traceback.format_exc())
        
        return convencoes
    
    def _parse_search_results(self, soup: BeautifulSoup, limit: int) -> List[Dict]:
        """Extrai convenções dos resultados da busca"""
        convencoes = []
        
        # Palavras-chave que indicam que NÃO é uma convenção (são links do menu)
        # Lista expandida com padrões específicos do site Mediador MTE
        menu_keywords = [
            'solicitação de registro', 'solicitar mediação', 'solicitação de mediação',
            'continuar solicitação', 'retificar solicitação', 'acompanhar solicitação',
            'acompanhar mediação', 'imprimir requerimento', 'manual do usuário',
            'cláusulas - grupos', 'cláusulas â grupos', 'cláusulas grupos',
            'protocolo sei mte', 'menu principal', 'navegação',
            'instrumentos coletivos registrados',  # Esta é uma página de listagem, não uma convenção
            'boas práticas trabalhistas', 'boas práticas',  # Página informativa
        ]
        
        def is_menu_item(text: str) -> bool:
            """Verifica se um texto é um item de menu"""
            if not text:
                return False
            text_lower = text.lower().strip()
            
            # Verificar padrões exatos de menu - ser mais específico
            exact_menu_matches = [
                'solicitação de registro de instrumento coletivo',
                'solicitação de mediação',
                'continuar solicitação',
                'retificar solicitação',
                'acompanhar solicitação',
                'acompanhar mediação',
                'imprimir requerimento',
                'manual do usuário',
                'instrumentos coletivos registrados',  # Esta é uma página de listagem
                'boas práticas trabalhistas',  # Página informativa
            ]
            
            # Verificar se é exatamente um item de menu conhecido
            if text_lower in exact_menu_matches:
                return True
            
            # Verificar padrões específicos no início do texto
            menu_patterns = [
                r'^continuar solicita[çc][ãa]o$',
                r'^retificar solicita[çc][ãa]o$',
                r'^acompanhar solicita[çc][ãa]o$',
                r'^solicitar media[çc][ãa]o$',
                r'^imprimir requerimento$',
                r'^manual do usuário$',
            ]
            
            for pattern in menu_patterns:
                if re.match(pattern, text_lower, re.I):
                    return True
            
            # Se o texto é muito curto (< 30 caracteres) e contém palavras de ação específicas, provavelmente é menu
            if len(text_lower) < 30 and any(kw in text_lower for kw in ['continuar', 'retificar', 'acompanhar', 'imprimir']):
                return True
            
            return False
        
        try:
            # Estratégia 1: Buscar em tabelas de resultados
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')[1:]  # Pular cabeçalho
                for row in rows[:limit * 2]:  # Buscar mais para filtrar depois
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 3:
                        convencao = self._parse_table_row(cells)
                        if convencao:
                            # Filtrar apenas se for claramente um item de menu
                            titulo_conv = convencao.get('titulo', '')
                            if not is_menu_item(titulo_conv):
                                convencoes.append(convencao)
                                if len(convencoes) >= limit:
                                    break
                if len(convencoes) >= limit:
                    break
            
            # Estratégia 2: Buscar em divs com classes específicas de resultados
            if len(convencoes) < limit:
                result_divs = soup.find_all(['div', 'li'], class_=re.compile(r'result|item|convencao|instrumento|registro', re.I))
                for div in result_divs[:limit * 2]:
                    convencao = self._parse_div_result(div)
                    if convencao:
                        # Filtrar apenas se for claramente um item de menu
                        titulo_conv = convencao.get('titulo', '')
                        if not is_menu_item(titulo_conv):
                            # Verificar se não é duplicado
                            if not any(c.get('instrumento_id') == convencao.get('instrumento_id') for c in convencoes):
                                convencoes.append(convencao)
                                if len(convencoes) >= limit:
                                    break
            
            # Estratégia 3: Buscar links específicos de convenções (filtrar menu)
            if len(convencoes) < limit:
                # Buscar links que contenham padrões de IDs numéricos ou códigos
                all_links = soup.find_all('a', href=True)
                
                # Primeiro, tentar encontrar área de resultados (pode estar em uma div específica)
                # Excluir áreas de menu/navegação
                result_containers = soup.find_all(['div', 'section', 'main'], 
                    class_=re.compile(r'result|lista|tabela|conteudo|content|main', re.I))
                
                # Excluir containers de menu/navegação
                result_containers = [c for c in result_containers 
                    if not any(kw in c.get('class', []) for kw in ['menu', 'nav', 'navigation', 'sidebar'])]
                
                links_to_check = []
                if result_containers:
                    # Se encontrou containers de resultados, buscar links dentro deles
                    for container in result_containers:
                        links_to_check.extend(container.find_all('a', href=True))
                else:
                    # Caso contrário, verificar todos os links, mas excluir áreas de menu
                    nav_areas = soup.find_all(['nav', 'div'], class_=re.compile(r'menu|nav|navigation', re.I))
                    nav_links = set()
                    for nav in nav_areas:
                        nav_links.update([l for l in nav.find_all('a', href=True)])
                    
                    links_to_check = [l for l in all_links if l not in nav_links]
                
                for link in links_to_check:
                    href = link.get('href', '')
                    text = link.get_text(strip=True)
                    
                    # Pular links de menu ANTES de processar
                    if is_menu_item(text) or is_menu_item(href):
                        continue
                    
                    # Procurar por padrões que indicam convenção real
                    # Aceitar links com IDs numéricos (4+ dígitos) OU padrões específicos de convenção
                    # Ser menos restritivo para encontrar mais resultados
                    has_valid_id = re.search(r'/\d{4,}', href) or re.search(r'[=/:](\d{4,})', href) or re.search(r'\d{4,}', href)
                    has_instrumento_pattern = (
                        re.search(r'instrumento', href, re.I) or 
                        re.search(r'convencao', href, re.I) or
                        re.search(r'/ConvencaoColetiva/', href, re.I) or
                        re.search(r'registro', href, re.I)
                    )
                    
                    # Se não tem ID válido nem padrão de instrumento, ainda tentar processar se o texto não for menu
                    # (ser menos restritivo)
                    if not has_valid_id and not has_instrumento_pattern:
                        # Ainda assim, tentar processar se o texto não for claramente um item de menu
                        if not is_menu_item(text):
                            # Processar mesmo sem padrão específico
                            pass
                        else:
                            continue
                    
                    convencao = self._parse_link_result(link)
                    if convencao:
                        # Filtrar novamente após parse (pode ter detectado menu no título)
                        titulo_conv = convencao.get('titulo', '')
                        if not is_menu_item(titulo_conv):
                            # Verificar se não é duplicado
                            if not any(c.get('instrumento_id') == convencao.get('instrumento_id') for c in convencoes):
                                convencoes.append(convencao)
                                if len(convencoes) >= limit:
                                    break
            
        except Exception as e:
            logger.error(f"Erro ao fazer parse dos resultados: {e}")
        
        return convencoes
    
    def _parse_table_row(self, cells) -> Optional[Dict]:
        """Extrai dados de uma linha de tabela"""
        try:
            # Tentar extrair informações comuns
            texto_completo = ' '.join([cell.get_text(strip=True) for cell in cells])
            
            # Corrigir encoding - garantir UTF-8
            try:
                if 'Ã§' in texto_completo or 'Ã£' in texto_completo or 'Ã' in texto_completo:
                    texto_bytes = texto_completo.encode('latin-1', errors='ignore')
                    texto_completo = texto_bytes.decode('utf-8', errors='ignore')
            except:
                pass
            
            # Procurar por padrões comuns
            instrumento_id = None
            titulo = None
            data_publicacao = None
            municipio = None
            uf = None
            
            # Procurar ID em links ou texto
            for cell in cells:
                links = cell.find_all('a', href=True)
                for link in links:
                    href = link.get('href', '')
                    # Extrair ID da URL - aceitar qualquer número (ser menos restritivo)
                    match = re.search(r'/(\d{4,})', href) or re.search(r'[=/:](\d{4,})', href) or re.search(r'(\d{4,})', href)
                    if match:
                        instrumento_id = match.group(1)
                        link_texto = link.get_text(strip=True) or texto_completo[:100]
                        # Corrigir encoding do texto do link também
                        try:
                            if 'Ã§' in link_texto or 'Ã£' in link_texto or 'Ã' in link_texto:
                                link_bytes = link_texto.encode('latin-1', errors='ignore')
                                link_texto = link_bytes.decode('utf-8', errors='ignore')
                        except:
                            pass
                        titulo = link_texto
                        break
            
            # Procurar datas
            date_pattern = r'(\d{2}[/-]\d{2}[/-]\d{4})'
            dates = re.findall(date_pattern, texto_completo)
            if dates:
                try:
                    data_publicacao = parser.parse(dates[0], dayfirst=True).date().isoformat()
                except:
                    pass
            
            # Procurar município/UF
            uf_pattern = r'\b([A-Z]{2})\b'
            ufs = re.findall(uf_pattern, texto_completo)
            if ufs:
                uf = ufs[0]
            
            if instrumento_id or titulo:
                return {
                    'instrumento_id': instrumento_id or f"TEMP-{hash(texto_completo) % 1000000}",
                    'titulo': titulo or texto_completo[:200],
                    'data_publicacao': data_publicacao,
                    'municipio': municipio,
                    'uf': uf,
                    'fonte': 'mediador_mte',
                    'texto_extraido': texto_completo[:500] if len(texto_completo) > 100 else None,
                }
        except Exception as e:
            logger.debug(f"Erro ao fazer parse de linha: {e}")
        
        return None
    
    def _parse_div_result(self, div) -> Optional[Dict]:
        """Extrai dados de um div de resultado"""
        try:
            texto = div.get_text(strip=True)
            if len(texto) < 10:  # Muito curto, provavelmente não é um resultado válido
                return None
            
            # Corrigir encoding - garantir UTF-8
            try:
                if 'Ã§' in texto or 'Ã£' in texto or 'Ã' in texto:
                    texto_bytes = texto.encode('latin-1', errors='ignore')
                    texto = texto_bytes.decode('utf-8', errors='ignore')
            except:
                pass
            
            # Filtrar divs de menu - ser mais específico
            texto_lower = texto.lower().strip()
            menu_patterns = [
                r'^continuar solicitação$',
                r'^retificar solicitação$',
                r'^acompanhar solicitação$',
                r'^solicitar mediação$',
            ]
            
            # Verificar se é exatamente um item de menu
            is_menu = any(re.match(pattern, texto_lower, re.I) for pattern in menu_patterns)
            if is_menu:
                return None
            
            # Procurar link dentro do div
            link = div.find('a', href=True)
            instrumento_id = None
            titulo = texto[:200]
            
            if link:
                href = link.get('href', '')
                # Procurar por IDs numéricos (4+ dígitos para ser menos restritivo)
                match = re.search(r'/(\d{4,})', href)
                if match:
                    instrumento_id = match.group(1)
                    link_texto = link.get_text(strip=True) or titulo
                    # Corrigir encoding do texto do link também
                    try:
                        if 'Ã§' in link_texto or 'Ã£' in link_texto or 'Ã' in link_texto:
                            link_bytes = link_texto.encode('latin-1', errors='ignore')
                            link_texto = link_bytes.decode('utf-8', errors='ignore')
                    except:
                        pass
                    titulo = link_texto
            
            # Retornar resultado se encontrou ID OU se o texto parece ser uma convenção válida
            if instrumento_id or (len(texto) > 20 and not any(kw in texto_lower for kw in ['continuar', 'retificar', 'acompanhar'])):
                return {
                    'instrumento_id': instrumento_id or f"TEMP-{hash(texto) % 1000000}",
                    'titulo': titulo,
                    'fonte': 'mediador_mte',
                    'texto_extraido': texto[:500],
                }
            
            return None
        except:
            return None
    
    def _parse_link_result(self, link) -> Optional[Dict]:
        """Extrai dados de um link de resultado"""
        try:
            href = link.get('href', '')
            texto = link.get_text(strip=True)
            
            if not texto or len(texto) < 5:
                return None
            
            # Corrigir encoding - garantir UTF-8
            try:
                # Se o texto parece estar mal codificado, tentar corrigir
                if 'Ã§' in texto or 'Ã£' in texto or 'Ã' in texto:
                    # Tentar decodificar como latin-1 e re-encodar como UTF-8
                    texto_bytes = texto.encode('latin-1', errors='ignore')
                    texto = texto_bytes.decode('utf-8', errors='ignore')
            except:
                pass
            
            # Extrair ID da URL - aceitar qualquer número (ser menos restritivo)
            match = re.search(r'/(\d{4,})', href) or re.search(r'[=/:](\d{4,})', href) or re.search(r'(\d{4,})', href)
            instrumento_id = match.group(1) if match else f"TEMP-{hash(href) % 1000000}"
            
            return {
                'instrumento_id': instrumento_id,
                'titulo': texto,
                'fonte': 'mediador_mte',
            }
        except:
            return None
    
    def get_convencao_details(self, instrumento_id: str) -> Optional[Dict]:
        """Busca detalhes de uma convenção específica"""
        try:
            # Tentar diferentes padrões de URL
            urls = [
                f"{self.base_url}/ConvencaoColetiva/Detalhes/{instrumento_id}",
                f"{self.base_url}/instrumento/{instrumento_id}",
                f"{self.base_url}/ConvencaoColetiva/Visualizar/{instrumento_id}",
            ]
            
            for url in urls:
                try:
                    response = self.session.get(url, timeout=30)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        return self._parse_detail_page(soup, instrumento_id)
                except:
                    continue
            
        except Exception as e:
            logger.error(f"Erro ao buscar detalhes da convenção {instrumento_id}: {e}")
        
        return None
    
    def _parse_detail_page(self, soup: BeautifulSoup, instrumento_id: str) -> Dict:
        """Extrai detalhes de uma página de convenção"""
        detalhes = {
            'instrumento_id': instrumento_id,
            'fonte': 'mediador_mte',
        }
        
        try:
            # Extrair título
            title = soup.find(['h1', 'h2', 'h3'], class_=re.compile(r'titulo|title', re.I))
            if title:
                detalhes['titulo'] = title.get_text(strip=True)
            
            # Extrair informações de campos comuns
            # Procurar por labels e valores
            labels = soup.find_all(['label', 'span', 'div'], string=re.compile(r'data|publicação|município|uf|cnae|sindicato', re.I))
            for label in labels:
                parent = label.find_parent()
                if parent:
                    value = parent.get_text(strip=True)
                    # Extrair valor após o label
                    value = value.split(':', 1)[-1].strip() if ':' in value else value
                    
                    label_text = label.get_text(strip=True).lower()
                    if 'data' in label_text or 'publicação' in label_text:
                        try:
                            detalhes['data_publicacao'] = parser.parse(value, dayfirst=True).date().isoformat()
                        except:
                            pass
                    elif 'município' in label_text:
                        detalhes['municipio'] = value
                    elif 'uf' in label_text or 'estado' in label_text:
                        detalhes['uf'] = value[:2].upper()
                    elif 'cnae' in label_text:
                        detalhes['cnae'] = value.replace('-', '').replace('/', '')[:7]
                    elif 'sindicato' in label_text and 'empregador' in label_text:
                        detalhes['sindicato_empregador'] = value
                    elif 'sindicato' in label_text and 'trabalhador' in label_text:
                        detalhes['sindicato_trabalhador'] = value
            
            # Extrair texto completo
            texto = soup.get_text(separator=' ', strip=True)
            detalhes['texto_extraido'] = texto[:1000000] if len(texto) > 100 else None
            
        except Exception as e:
            logger.error(f"Erro ao fazer parse da página de detalhes: {e}")
        
        return detalhes

