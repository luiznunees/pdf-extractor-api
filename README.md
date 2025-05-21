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
uvicorn backend.app:app --reload
```

## Deploy

O projeto está configurado para deploy automático na Vercel. 