import pdfplumber
import re
from typing import List, Dict, Optional
from services.logger import parser_logger

class GuaridaParser:
    def __init__(self):
        self.name_patterns = [
            # Pattern for names after "Condomino - Endereço"
            r'Condomino - Endereço\s*([A-Z\s.-]+?)(?:\s*$|\s*R\s|$)',
            # Pattern for names in the first line after number
            r'^\s*\d+\s+([A-Z\s.-]+?)\s*(?:Loft|Loja|Apto|Casa|Sala|Box|Terreno|Cobertura|Depot|Garagem|Área|Lotes)',
        ]
        
        self.phone_patterns = [
            # Pattern for cell phone
            r'Cel\.:\s*(\(?\d{2}\)?\s*\d{4,5}[-.\s]?\d{4})',
            # Pattern for landline (fallback)
            r'Tel\.:\s*(\(?\d{2}\)?\s*\d{4}[-.\s]?\d{4})',
        ]
        parser_logger.info("Initialized GuaridaParser with patterns")
    
    def parse(self, pdf_path: str) -> List[Dict[str, str]]:
        """
        Parse a Guarida PDF file and extract owner names and phone numbers.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List[Dict[str, str]]: List of dictionaries containing owner names and phone numbers
        """
        parser_logger.info(f"Starting to parse PDF: {pdf_path}")
        extracted_data = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                parser_logger.info(f"PDF has {total_pages} pages")
                
                for page_num, page in enumerate(pdf.pages, 1):
                    parser_logger.info(f"Processing page {page_num}/{total_pages}")
                    
                    # Extract text with preserved structure
                    text = page.extract_text(x_tolerance=2, y_tolerance=2)
                    if not text:
                        parser_logger.warning(f"No text extracted from page {page_num}")
                        continue
                    
                    # Split into blocks (separated by double newlines)
                    blocks = text.split('\n\n')
                    parser_logger.info(f"Found {len(blocks)} blocks on page {page_num}")
                    
                    for block_num, block in enumerate(blocks, 1):
                        if not block.strip():
                            continue
                        
                        # Extract owner name
                        owner_name = self._extract_owner_name(block)
                        if not owner_name:
                            parser_logger.debug(f"No owner name found in block {block_num} on page {page_num}")
                            continue
                        
                        # Extract phone number
                        phone = self._extract_phone(block)
                        if not phone:
                            parser_logger.debug(f"No phone number found for owner: {owner_name}")
                        
                        extracted_data.append({
                            "Nome do Proprietário": owner_name.strip(),
                            "Celular": phone if phone else ""
                        })
                        parser_logger.debug(f"Extracted data for owner: {owner_name}")
            
            parser_logger.info(f"Successfully parsed PDF. Extracted {len(extracted_data)} records")
            return extracted_data
            
        except Exception as e:
            parser_logger.error(f"Error parsing PDF: {str(e)}", exc_info=True)
            raise
    
    def _extract_owner_name(self, block: str) -> Optional[str]:
        """Extract the owner name from a block of text."""
        for pattern in self.name_patterns:
            match = re.search(pattern, block, re.MULTILINE)
            if match:
                name = match.group(1).strip()
                # Clean up the name
                name = re.sub(r'\s+', ' ', name)  # Replace multiple spaces with single space
                name = name.strip()
                if name:
                    return name
        return None
    
    def _extract_phone(self, block: str) -> Optional[str]:
        """Extract the phone number from a block of text."""
        for pattern in self.phone_patterns:
            match = re.search(pattern, block)
            if match:
                phone = match.group(1)
                # Clean up the phone number (remove non-numeric characters)
                phone = re.sub(r'[^0-9]', '', phone)
                if phone:
                    return phone
        return None 