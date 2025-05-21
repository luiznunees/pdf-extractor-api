from parsers.guarida_parser import GuaridaParser
from services.data_formatter import format_to_csv
from services.logger import app_logger
import os

def process_pdf(pdf_path: str, provider_name: str) -> str:
    """
    Process a PDF file and return the extracted data in CSV format.
    
    Args:
        pdf_path: Path to the PDF file
        provider_name: Name of the provider (e.g., "guarida")
        
    Returns:
        str: CSV formatted data
    """
    app_logger.info(f"Starting PDF processing for provider: {provider_name}")
    
    if not os.path.exists(pdf_path):
        app_logger.error(f"PDF file not found: {pdf_path}")
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    # Select the appropriate parser based on provider
    if provider_name.lower() == "guarida":
        app_logger.info("Using GuaridaParser for processing")
        parser = GuaridaParser()
    else:
        app_logger.error(f"Unsupported provider: {provider_name}")
        raise ValueError(f"Unsupported provider: {provider_name}")
    
    try:
        # Extract data using the parser
        app_logger.info("Extracting data from PDF")
        extracted_data = parser.parse(pdf_path)
        app_logger.info(f"Successfully extracted {len(extracted_data)} records")
        
        # Format the data as CSV
        app_logger.info("Formatting data to CSV")
        csv_data = format_to_csv(extracted_data)
        app_logger.info("CSV formatting completed")
        
        return csv_data
    except Exception as e:
        app_logger.error(f"Error processing PDF: {str(e)}", exc_info=True)
        raise 