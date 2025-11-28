"""
Scraper service for collecting convenções from Mediador MTE
"""
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Dict, Optional
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class MediadorScraper:
    """Scraper for Mediador MTE website"""
    
    def __init__(self):
        self.base_url = settings.MEDIADOR_BASE_URL
        self.delay = settings.SCRAPER_DELAY_SECONDS
        self.user_agent = settings.SCRAPER_USER_AGENT
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.user_agent
        })
    
    def get_driver(self):
        """Get Selenium WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument(f'user-agent={self.user_agent}')
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    
    def extract_instrumento_ids(self, search_params: Optional[Dict] = None) -> List[str]:
        """
        Extract instrumento IDs from Mediador MTE
        
        Args:
            search_params: Dictionary with search parameters (municipio, cnae, etc.)
        
        Returns:
            List of instrumento IDs
        """
        instrumento_ids = []
        
        try:
            # Try multiple strategies to find instrumento IDs
            
            # Strategy 1: Try direct API/JSON endpoint if available
            try:
                # Common API patterns for government sites
                api_urls = [
                    f"{self.base_url}/api/instrumentos",
                    f"{self.base_url}/api/convencoes",
                    f"{self.base_url}/api/v1/instrumentos",
                ]
                
                for api_url in api_urls:
                    try:
                        response = self.session.get(api_url, timeout=10)
                        if response.status_code == 200:
                            data = response.json()
                            if isinstance(data, list):
                                for item in data:
                                    if isinstance(item, dict) and 'id' in item:
                                        instrumento_ids.append(str(item['id']))
                                    elif isinstance(item, str):
                                        instrumento_ids.append(item)
                            elif isinstance(data, dict) and 'results' in data:
                                for item in data['results']:
                                    if isinstance(item, dict) and 'id' in item:
                                        instrumento_ids.append(str(item['id']))
                            
                            if instrumento_ids:
                                logger.info(f"Found {len(instrumento_ids)} IDs via API: {api_url}")
                                return list(set(instrumento_ids))  # Remove duplicates
                    except:
                        continue
            except Exception as e:
                logger.debug(f"API strategy failed: {e}")
            
            # Strategy 2: Use Selenium for dynamic content
            try:
                driver = self.get_driver()
                
                # Try different search URLs
                search_urls = [
                    f"{self.base_url}/busca",
                    f"{self.base_url}/pesquisa",
                    f"{self.base_url}/instrumentos",
                    f"{self.base_url}/convencoes",
                ]
                
                for search_url in search_urls:
                    try:
                        driver.get(search_url)
                        time.sleep(self.delay * 2)  # Wait longer for dynamic content
                        
                        # Try multiple selectors
                        selectors = [
                            "a[href*='/instrumento/']",
                            "a[href*='instrumento']",
                            ".instrumento-link",
                            ".convencao-link",
                            "[data-instrumento-id]",
                        ]
                        
                        for selector in selectors:
                            try:
                                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                                for element in elements:
                                    href = element.get_attribute('href')
                                    if href:
                                        # Extract ID from URL
                                        parts = href.split('/')
                                        if 'instrumento' in parts:
                                            idx = parts.index('instrumento')
                                            if idx + 1 < len(parts):
                                                instrumento_id = parts[idx + 1].split('?')[0].split('#')[0]
                                                if instrumento_id and instrumento_id not in instrumento_ids:
                                                    instrumento_ids.append(instrumento_id)
                                    
                                    # Also try data attributes
                                    data_id = element.get_attribute('data-instrumento-id')
                                    if data_id and data_id not in instrumento_ids:
                                        instrumento_ids.append(data_id)
                                
                                if instrumento_ids:
                                    break
                            except:
                                continue
                        
                        if instrumento_ids:
                            break
                    except Exception as e:
                        logger.debug(f"Failed to extract from {search_url}: {e}")
                        continue
                
                driver.quit()
                
            except Exception as e:
                logger.warning(f"Selenium strategy failed: {e}")
                if 'driver' in locals():
                    try:
                        driver.quit()
                    except:
                        pass
            
            # Strategy 3: Try simple HTTP request with BeautifulSoup
            if not instrumento_ids:
                try:
                    search_urls = [
                        f"{self.base_url}/busca",
                        f"{self.base_url}/pesquisa",
                        f"{self.base_url}/instrumentos",
                        f"{self.base_url}/convencoes",
                        f"{self.base_url}/",
                    ]
                    
                    for search_url in search_urls:
                        try:
                            response = self.session.get(search_url, timeout=30)
                            if response.status_code == 200:
                                soup = BeautifulSoup(response.content, 'html.parser')
                                
                                # Find all links containing 'instrumento'
                                links = soup.find_all('a', href=True)
                                for link in links:
                                    href = link.get('href', '')
                                    if '/instrumento/' in href or 'instrumento' in href.lower():
                                        parts = href.split('/')
                                        if 'instrumento' in parts:
                                            idx = parts.index('instrumento')
                                            if idx + 1 < len(parts):
                                                instrumento_id = parts[idx + 1].split('?')[0].split('#')[0]
                                                if instrumento_id and instrumento_id not in instrumento_ids:
                                                    instrumento_ids.append(instrumento_id)
                                
                                # Also try to find IDs in data attributes or text content
                                elements_with_data = soup.find_all(attrs={'data-id': True})
                                for elem in elements_with_data:
                                    data_id = elem.get('data-id')
                                    if data_id and data_id not in instrumento_ids:
                                        instrumento_ids.append(str(data_id))
                                
                                # Try to find IDs in JavaScript/JSON embedded in page
                                scripts = soup.find_all('script')
                                for script in scripts:
                                    if script.string:
                                        import re
                                        # Look for patterns like "instrumento_id": "123" or instrumento/123
                                        matches = re.findall(r'instrumento[_-]?id["\']?\s*[:=]\s*["\']?(\d+)', script.string, re.IGNORECASE)
                                        matches.extend(re.findall(r'/instrumento/(\d+)', script.string))
                                        for match in matches:
                                            if match and match not in instrumento_ids:
                                                instrumento_ids.append(match)
                                
                                if instrumento_ids:
                                    logger.info(f"Found IDs via BeautifulSoup from {search_url}")
                                    break
                        except Exception as e:
                            logger.debug(f"Failed to extract from {search_url}: {e}")
                            continue
                except Exception as e:
                    logger.debug(f"HTTP/BeautifulSoup strategy failed: {e}")
            
            # Remove duplicates and return
            instrumento_ids = list(set(instrumento_ids))
            logger.info(f"Extracted {len(instrumento_ids)} instrumento IDs")
            
        except Exception as e:
            logger.error(f"Error extracting instrumento IDs: {e}")
        
        return instrumento_ids
    
    def extract_metadados(self, instrumento_id: str) -> Optional[Dict]:
        """
        Extract metadata from convenção detail page
        
        Args:
            instrumento_id: ID of the instrumento coletivo
        
        Returns:
            Dictionary with metadata or None if error
        """
        try:
            # Try multiple URL patterns
            urls = [
                f"{self.base_url}/instrumento/{instrumento_id}",
                f"{self.base_url}/convencao/{instrumento_id}",
                f"{self.base_url}/detalhes/{instrumento_id}",
            ]
            
            soup = None
            for url in urls:
                try:
                    response = self.session.get(url, timeout=30)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        break
                except:
                    continue
            
            if not soup:
                logger.warning(f"Could not access page for instrumento {instrumento_id}")
                return None
            
            # Try multiple selectors for each field
            metadados = {
                'instrumento_id': instrumento_id,
                'titulo': self._extract_text_multiple(soup, [
                    'h1.titulo', 'h1', '.titulo', '.title', 
                    '[class*="titulo"]', '[class*="title"]'
                ]) or f"Convenção {instrumento_id}",
                'data_publicacao': self._extract_date_multiple(soup, [
                    'span.data-publicacao', '.data-publicacao', '[class*="data-publicacao"]',
                    'span.data', '.data-publicacao', 'time[datetime]'
                ]),
                'vigencia_inicio': self._extract_date_multiple(soup, [
                    'span.vigencia-inicio', '.vigencia-inicio', '[class*="vigencia-inicio"]',
                    'span.vigencia', '.inicio'
                ]),
                'vigencia_fim': self._extract_date_multiple(soup, [
                    'span.vigencia-fim', '.vigencia-fim', '[class*="vigencia-fim"]',
                    'span.fim', '.fim'
                ]),
                'sindicato_empregador': self._extract_text_multiple(soup, [
                    'div.sindicato-empregador', '.sindicato-empregador',
                    '[class*="sindicato-empregador"]', '[class*="empregador"]'
                ]),
                'sindicato_trabalhador': self._extract_text_multiple(soup, [
                    'div.sindicato-trabalhador', '.sindicato-trabalhador',
                    '[class*="sindicato-trabalhador"]', '[class*="trabalhador"]'
                ]),
                'municipio': self._extract_text_multiple(soup, [
                    'span.municipio', '.municipio', '[class*="municipio"]',
                    'span.cidade', '.cidade'
                ]),
                'uf': self._extract_text_multiple(soup, [
                    'span.uf', '.uf', '[class*="uf"]', 'span.estado', '.estado'
                ]),
                'cnae': self._extract_text_multiple(soup, [
                    'span.cnae', '.cnae', '[class*="cnae"]'
                ]),
                'documento_url': self._extract_link_multiple(soup, [
                    'a.download-documento', 'a[href*=".pdf"]', 'a[href*="download"]',
                    'a.baixar', '.download-link'
                ]),
            }
            
            time.sleep(self.delay)  # Be respectful
            
            return metadados
            
        except Exception as e:
            logger.error(f"Error extracting metadata for {instrumento_id}: {e}")
            return None
    
    def download_documento(self, url: str, instrumento_id: str) -> Optional[tuple]:
        """
        Download documento from URL
        
        Args:
            url: URL of the document
            instrumento_id: ID for naming the file
        
        Returns:
            Tuple of (filepath, extension) or None if error
        """
        try:
            response = self.session.get(url, timeout=60)
            response.raise_for_status()
            
            # Determine file extension
            content_type = response.headers.get('content-type', '').lower()
            if 'pdf' in content_type:
                ext = '.pdf'
            elif 'html' in content_type:
                ext = '.html'
            else:
                ext = '.pdf'  # default
            
            # Save to temporary location
            import os
            os.makedirs('temp_downloads', exist_ok=True)
            filepath = f"temp_downloads/{instrumento_id}{ext}"
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return (filepath, ext)
            
        except Exception as e:
            logger.error(f"Error downloading documento from {url}: {e}")
            return None
    
    def _extract_text(self, soup: BeautifulSoup, selector: str) -> Optional[str]:
        """Extract text from HTML element"""
        element = soup.select_one(selector)
        return element.get_text(strip=True) if element else None
    
    def _extract_date(self, soup: BeautifulSoup, selector: str) -> Optional[str]:
        """Extract date from HTML element"""
        text = self._extract_text(soup, selector)
        if text:
            # Parse date format (adjust as needed)
            from dateutil import parser
            try:
                return parser.parse(text, dayfirst=True).date().isoformat()
            except:
                return None
        return None
    
    def _extract_link(self, soup: BeautifulSoup, selector: str) -> Optional[str]:
        """Extract link from HTML element"""
        element = soup.select_one(selector)
        if element:
            href = element.get('href')
            if href:
                if href.startswith('http'):
                    return href
                else:
                    return f"{self.base_url}{href}"
        return None
    
    def _extract_text_multiple(self, soup: BeautifulSoup, selectors: List[str]) -> Optional[str]:
        """Try multiple selectors to extract text"""
        for selector in selectors:
            text = self._extract_text(soup, selector)
            if text:
                return text
        return None
    
    def _extract_date_multiple(self, soup: BeautifulSoup, selectors: List[str]) -> Optional[str]:
        """Try multiple selectors to extract date"""
        for selector in selectors:
            date = self._extract_date(soup, selector)
            if date:
                return date
        return None
    
    def _extract_link_multiple(self, soup: BeautifulSoup, selectors: List[str]) -> Optional[str]:
        """Try multiple selectors to extract link"""
        for selector in selectors:
            link = self._extract_link(soup, selector)
            if link:
                return link
        return None

