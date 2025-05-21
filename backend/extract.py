import PyPDF2
import re
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Owner:
    owner_name: str
    phone: str

class PDFExtractor:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.text = ""
        self.owners: List[Owner] = []

    def extract_text(self):
        """Extract text from PDF file"""
        with open(self.pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                self.text += page.extract_text()
        return self.text

    def parse_owners(self):
        """Parse the extracted text to find owner information"""
        # Split text into lines
        lines = self.text.split('\n')
        
        current_owner = None
        for line in lines:
            # Skip header lines
            if "Protocolo de Entrega de Correspondência" in line:
                continue
                
            # Look for unit/box number pattern to identify new owner
            unit_match = re.search(r'(?:Loja|Box)\s+(\w+\s*\d+)', line)
            if unit_match:
                if current_owner:
                    self.owners.append(current_owner)
                
                # Start new owner entry
                current_owner = Owner(
                    owner_name="",
                    phone=""
                )
                continue

            if current_owner:
                # Extract only cell phone
                phone_match = re.search(r'Cel\.:\s*([\d\(\)\s\.\-]+)', line)
                if phone_match:
                    current_owner.phone = phone_match.group(1).strip()
                    continue

                # If no specific pattern matches and no owner name yet, it's probably the name
                if not current_owner.owner_name and line.strip() and not any(x in line.lower() for x in ['cpf:', 'cel.:', 'tel.:', 'email:']):
                    current_owner.owner_name = line.strip()

        # Add the last owner if exists
        if current_owner:
            self.owners.append(current_owner)

    def process(self):
        """Process the PDF and return extracted data"""
        self.extract_text()
        self.parse_owners()
        return self.owners

def main():
    # Example usage
    extractor = PDFExtractor("backend/exemplo.pdf")
    owners = extractor.process()
    
    # Print results
    for owner in owners:
        print(f"Nome: {owner.owner_name}")
        print(f"Celular: {owner.phone}")
        print("-" * 50)

if __name__ == "__main__":
    main() 