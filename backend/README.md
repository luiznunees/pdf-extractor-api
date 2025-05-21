# Property Listing Extractor Backend

This is the backend service for the Property Listing Extractor system. It provides an API for processing PDF files containing property listings and extracting owner information.

## Features

- PDF file upload and processing
- Extraction of owner names and phone numbers from Guarida property listings
- CSV output generation
- RESTful API endpoints
- Job status tracking
- CORS support for frontend integration

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

Start the server with:
```bash
python app.py
```

The server will start on `http://localhost:8000`

## API Endpoints

### POST /api/upload
Upload a PDF file for processing.

**Parameters:**
- `file`: PDF file (multipart/form-data)
- `provider_name`: String (default: "guarida")

**Response:**
```json
{
    "job_id": "uuid",
    "status": "completed",
    "download_url": "/api/download/uuid"
}
```

### GET /api/status/{job_id}
Check the status of a processing job.

**Response:**
```json
{
    "job_id": "uuid",
    "status": "completed|processing|failed",
    "download_url": "/api/download/uuid",
    "error": "error message (if failed)"
}
```

### GET /api/download/{job_id}
Download the processed CSV file.

**Response:**
- CSV file download

## Project Structure

```
backend/
├── app.py              # Main FastAPI application
├── requirements.txt    # Project dependencies
├── parsers/
│   ├── __init__.py
│   └── guarida_parser.py  # Guarida PDF parser implementation
├── services/
│   ├── processing_service.py  # PDF processing orchestration
│   ├── data_formatter.py     # CSV formatting
│   └── job_manager.py        # Job status management
└── temp/               # Temporary file storage
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