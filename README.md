# RAG-Based Architecture Research Assistant

## Overview

This project implements a complete end-to-end RAG system:

- Extracts data from both digital and scanned PDFs  
- Cleans and filters noisy architectural text  
- Splves data into token-aware chunks  
- Converts text into vector embeddings  
- Stores embeddings in ChromaDB  
- Retrieves relevant context for queries  
- Generates grounded responses using a local LLM  
- Exposes functionality through a FastAPI backend and CLI  

---

## System Architecture


PDF Files
│
▼
Data Cleaning Pipeline (OCR + Deduplication + Filtering)
│
▼
Token-Aware Chunking (Sliding Window + Overlap)
│
▼
JSONL Dataset (Chunks + Metadata)
│
▼
Embedding Model (Sentence Transformers)
│
▼
Vector Database (ChromaDB)
│
▼
RAG Pipeline (Retrieve + Prompt + LLM)
│
▼
API Layer / CLI Interface


---

## Project Structure


├── data_pipeline/
│ ├── clean_pdfs.py
│ ├── chunk_jsonl.py
│
├── backend/
│ ├── init.py
│ ├── config.py
│ ├── embedding_utils.py
│ ├── database.py
│ ├── rag_pipeline.py
│ ├── api.py
│ ├── main.py
│
├── chroma_db/
├── requirements.py
└── README.md


---

## Data Pipeline

### 1. Hybrid PDF Extraction

The system first attempts text extraction using PyMuPDF.  
If no usable text is found, it falls back to OCR.

```python
if not text.strip():
    text = extract_text_with_ocr(page)

This ensures robustness when dealing with scanned or image-based PDFs.

2. Deduplication

Each extracted page is hashed using MD5:

text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()

Prevents duplicate storage and improves efficiency.

3. Noise Filtering

Low-quality text is filtered:

if alpha_chars / len(text) < 0.3:
    return True
4. Token-Aware Chunking
Uses tokenizer aligned with embedding model
Maintains chunk size within limits
Uses overlap to preserve context
JSONL Format
{
  "doc_id": "25845916",
  "file": "25845916.pdf",
  "category": "misc",
  "page_span": [1, 1],
  "text": "...",
  "chunk_hash": "abc123"
}
API Usage
Endpoint
POST /query
Request
{
  "query": "What are fire safety regulations?"
}
Response
{
  "answer": "...",
  "sources": [...]
}
Run Locally
# Install dependencies
python requirements.py

# Initialize database
python main.py --init

# Start API
uvicorn api:app --reload
