# RAG-Based Architecture Research Assistant

## Overview

This project implements a complete end-to-end Retrieval-Augmented Generation (RAG) system designed to process architectural PDFs and answer user queries using a grounded Large Language Model (LLM).

The system is built to handle real-world, messy datasets and focuses on robustness, efficiency, and accuracy.

---

## System Architecture

```
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
```

---

## Data Pipeline

### 1. Hybrid PDF Extraction

The system first attempts to extract text using PyMuPDF. If no usable text is found, it falls back to OCR using Tesseract.

This ensures:
- Robust handling of scanned PDFs
- No data loss due to format inconsistencies

Example:
```python
if not text.strip():
    text = extract_text_with_ocr(page)
```

---

### 2. Deduplication

Each page is hashed using MD5 to prevent duplicate entries.

```python
text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
```

Benefits:
- Reduces storage usage
- Improves retrieval speed
- Prevents redundant embeddings

---

### 3. Noise Reduction

Text is cleaned using regex and heuristics:
- Removes boilerplate text (headers, footers, page numbers)
- Filters low-quality chunks

```python
if alpha_chars / len(text) < 0.3:
    return True
```

This improves the signal-to-noise ratio for better LLM responses.

---

### 4. Token-Aware Chunking

Instead of splitting text by characters, the system uses token-based chunking aligned with the embedding model.

Key features:
- Maintains token limits
- Uses sliding window with overlap
- Preserves context across chunks

---

## JSONL Dataset

Each chunk is stored as an independent JSON object:

```json
{
  "doc_id": "25845916",
  "file": "25845916.pdf",
  "category": "misc",
  "page_span": [1, 1],
  "text": "...",
  "chunk_hash": "abc123"
}
```

Advantages:
- Memory-efficient streaming
- Flexible metadata storage
- Scalable for large datasets

---

## Embedding Layer

The system uses Sentence Transformers to convert text into vector embeddings.

Model used:
- multi-qa-MiniLM-L6-cos-v1

Example:
```python
embedding = model.encode(text)
```

Purpose:
- Enables semantic similarity search
- Converts text into numerical representation

---

## Vector Database (ChromaDB)

Stores embeddings and enables fast similarity search.

Key features:
- Persistent local storage
- Automatic embedding integration
- Fault recovery mechanism

---

## RAG Pipeline

```
User Query
   │
   ▼
Convert to Embedding
   │
   ▼
Retrieve Top-K Relevant Chunks
   │
   ▼
Construct Prompt with Context
   │
   ▼
Generate Answer using LLM
```

---

## Prompt Engineering

The system uses strict prompts to prevent hallucination:

```
You are an expert in architecture research.
Use only the provided context.
```

---

## Performance Optimizations

### Pre-Warming
- Loads LLM into memory at startup
- Eliminates cold start delay

### Context Truncation
- Limits input size
- Prevents overflow
- Reduces latency

---

## API Layer

### Endpoint
POST /query

### Request
```json
{
  "query": "What are fire safety regulations?"
}
```

### Response
```json
{
  "answer": "...",
  "sources": [...]
}
```

Features:
- Input validation using Pydantic
- Error handling
- CORS support

---

## CLI Usage

Run queries directly:

```bash
python main.py --query "fire codes"
```

Commands:
- --init (initialize database)
- --query (single query)
- --interactive (chat mode)

---

## Project Structure

```
├── data_pipeline/
│   ├── clean_pdfs.py
│   ├── chunk_jsonl.py
│
├── backend/
│   ├── __init__.py
│   ├── config.py
│   ├── embedding_utils.py
│   ├── database.py
│   ├── rag_pipeline.py
│   ├── api.py
│   ├── main.py
│
├── chroma_db/
├── requirements.py
└── README.md
```

---

## Design Decisions

### Local Models
- Ensures privacy
- No API cost
- Works offline

### FastAPI
- Async performance
- Easy integration
- Auto documentation

### Sentence Transformers
- Optimized for semantic search
- Better for Q&A tasks

---

## Challenges Addressed

| Problem | Solution |
|--------|---------|
| Scanned PDFs | OCR fallback |
| Duplicate pages | Hashing |
| Context loss | Sliding window |
| Hallucination | Prompt constraints |
| Latency | Pre-warming |

---

## Future Improvements

- Add frontend (React/Next.js)
- Hybrid search (BM25 + vector)
- Re-ranking models
- Cloud deployment
- Authentication

---

## Setup

```bash
python requirements.py
python main.py --init
uvicorn api:app --reload
```

---

## Summary

This project demonstrates a complete RAG pipeline that transforms unstructured PDF data into a searchable knowledge base and generates grounded answers using a local LLM.
