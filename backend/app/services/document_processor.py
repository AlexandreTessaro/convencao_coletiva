"""
Document processing service for extracting text from HTML and PDFs
"""
import os
from typing import Optional, Tuple
from bs4 import BeautifulSoup
import PyPDF2
import pdfplumber
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Process documents to extract text"""
    
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD
    
    def extract_text(self, filepath: str, file_ext: str) -> Tuple[Optional[str], str]:
        """
        Extract text from document
        
        Args:
            filepath: Path to the document
            file_ext: File extension (.html, .pdf)
        
        Returns:
            Tuple of (extracted_text, document_type)
        """
        if file_ext == '.html':
            return self._extract_from_html(filepath), 'HTML'
        
        elif file_ext == '.pdf':
            # Try PDF digital first
            try:
                text = self._extract_from_pdf_digital(filepath)
                if text and len(text.strip()) > 100:
                    return text, 'PDF_DIGITAL'
            except Exception as e:
                logger.warning(f"Failed to extract as digital PDF: {e}")
            
            # Try OCR for scanned PDF
            try:
                text = self._extract_from_pdf_scanned(filepath)
                return text, 'PDF_ESCANEADO'
            except Exception as e:
                logger.error(f"Failed to extract from scanned PDF: {e}")
                return None, 'PDF_ESCANEADO'
        
        else:
            logger.error(f"Unsupported file type: {file_ext}")
            return None, 'UNKNOWN'
    
    def _extract_from_html(self, filepath: str) -> Optional[str]:
        """Extract text from HTML file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                html = f.read()
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # Remove scripts and styles
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract text
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
            
        except Exception as e:
            logger.error(f"Error extracting text from HTML: {e}")
            return None
    
    def _extract_from_pdf_digital(self, filepath: str) -> Optional[str]:
        """Extract text from digital PDF"""
        try:
            text = ""
            with open(filepath, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            return text if text.strip() else None
            
        except Exception as e:
            logger.error(f"Error extracting text from digital PDF: {e}")
            return None
    
    def _extract_from_pdf_scanned(self, filepath: str) -> Optional[str]:
        """Extract text from scanned PDF using OCR"""
        try:
            # Convert PDF to images
            images = convert_from_path(filepath, dpi=300)
            
            text = ""
            for image in images:
                # Preprocess image for better OCR
                image = self._preprocess_image(image)
                
                # Apply OCR
                page_text = pytesseract.image_to_string(
                    image,
                    lang=settings.OCR_LANG
                )
                text += page_text + "\n"
            
            return text if text.strip() else None
            
        except Exception as e:
            logger.error(f"Error extracting text from scanned PDF: {e}")
            return None
    
    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """Preprocess image for better OCR results"""
        # Convert to grayscale
        if image.mode != 'L':
            image = image.convert('L')
        
        # Enhance contrast (simple approach)
        # Can be enhanced with more sophisticated preprocessing
        
        return image

