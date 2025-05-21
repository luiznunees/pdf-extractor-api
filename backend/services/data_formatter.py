import csv
from io import StringIO
from typing import List, Dict
from services.logger import app_logger

def format_to_csv(data: List[Dict[str, str]]) -> str:
    """
    Format the extracted data as CSV.
    
    Args:
        data: List of dictionaries containing the extracted data
        
    Returns:
        str: CSV formatted data
    """
    app_logger.info(f"Formatting {len(data)} records to CSV")
    
    if not data:
        app_logger.warning("No data to format, returning empty CSV with headers")
        return "Nome do Proprietário,Celular\n"
    
    try:
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=["Nome do Proprietário", "Celular"])
        writer.writeheader()
        writer.writerows(data)
        
        csv_data = output.getvalue()
        app_logger.info("CSV formatting completed successfully")
        return csv_data
    except Exception as e:
        app_logger.error(f"Error formatting CSV: {str(e)}", exc_info=True)
        raise 