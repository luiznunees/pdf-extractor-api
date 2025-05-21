from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import uuid
import logging
from typing import List, Dict
from extract import PDFExtractor
from pydantic import BaseModel
from io import BytesIO

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PDF Extractor API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dicionário para armazenar os resultados das extrações
extractions: Dict[str, List[Dict[str, str]]] = {}

class OwnerResponse(BaseModel):
    owner_name: str
    phone: str

@app.post("/extract")
async def extract_pdf(file: UploadFile = File(...)):
    """
    Endpoint para extrair nome e celular de um PDF de protocolo de entrega de correspondência.
    Retorna um ID que pode ser usado para buscar os resultados posteriormente.
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são permitidos")
    
    # Gera um ID único para a extração
    extraction_id = str(uuid.uuid4())
    
    try:
        # Lê o conteúdo do arquivo em memória
        content = await file.read()
        pdf_file = BytesIO(content)
        
        # Processa o PDF
        extractor = PDFExtractor(pdf_file)
        owners = extractor.process()
        
        # Converte para o formato de resposta
        results = [
            {
                "owner_name": owner.owner_name,
                "phone": owner.phone
            } for owner in owners
        ]
        
        # Salva os resultados
        extractions[extraction_id] = results
        
        return {
            "extraction_id": extraction_id,
            "message": "Extração concluída com sucesso",
            "count": len(results)
        }
        
    except Exception as e:
        logger.error(f"Erro ao processar PDF: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/results/{extraction_id}", response_model=List[OwnerResponse])
async def get_results(extraction_id: str):
    """
    Endpoint para buscar os resultados de uma extração usando o ID.
    """
    if extraction_id not in extractions:
        raise HTTPException(status_code=404, detail="Extração não encontrada")
    
    return extractions[extraction_id]

@app.get("/")
async def root():
    """
    Endpoint raiz para verificar se a API está funcionando.
    """
    return {"message": "API de extração de PDF está funcionando!"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Iniciando servidor da API de extração de PDF")
    uvicorn.run(app, host="0.0.0.0", port=8000) 