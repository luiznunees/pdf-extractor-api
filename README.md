# PDF Extractor API

API para extração de informações de PDFs de protocolos de entrega de correspondência.

## Funcionalidades

- Extração de nomes e números de telefone de PDFs
- API REST com FastAPI
- Endpoints para upload e consulta de resultados

## Endpoints

### POST /extract
Upload de arquivo PDF para extração de informações.

### GET /results/{extraction_id}
Consulta dos resultados de uma extração específica.

## Tecnologias

- Python 3.8+
- FastAPI
- PyPDF2
- Vercel (Deploy)

## Instalação

1. Clone o repositório
```bash
git clone [URL_DO_REPOSITÓRIO]
```

2. Instale as dependências
```bash
pip install -r requirements.txt
```

3. Execute o servidor
```bash
uvicorn app:app --reload
```

## Deploy

O projeto está configurado para deploy automático na Vercel. Para fazer o deploy:

1. Faça push do código para o GitHub
2. Importe o repositório na Vercel
3. O deploy será feito automaticamente

## Estrutura do Projeto

```
.
├── app.py              # Aplicação FastAPI
├── extract.py          # Lógica de extração de PDF
├── requirements.txt    # Dependências do projeto
└── vercel.json         # Configuração do Vercel
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:
- 400: Bad Request (e.g., invalid file type)
- 404: Not Found (e.g., job not found)
- 500: Internal Server Error (e.g., processing error)

## Notes

- The `temp` directory is used for storing temporary files. It should be cleaned up periodically.
- The service currently supports only Guarida property listings.
- Phone numbers are standardized to contain only digits. 