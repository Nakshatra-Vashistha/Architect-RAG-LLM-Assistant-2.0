RAG-Based Architecture Research Assistant

A production-grade Retrieval-Augmented Generation (RAG) system designed to process architectural PDFs, extract structured knowledge, and answer user queries using a grounded large language model pipeline.

Overview

This project implements a complete end-to-end RAG system:

Extracts data from both digital and scanned PDFs
Cleans and filters noisy architectural text
Splits data into token-aware chunks
Converts text into vector embeddings
Stores embeddings in ChromaDB
Retrieves relevant context for queries
Generates grounded responses using a local LLM
Exposes functionality through a FastAPI backend and CLI
System Architecture
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
Key Features
Fault-Tolerant PDF Processing
Uses PyMuPDF for primary extraction
Falls back to Tesseract OCR for scanned pages
Handles mixed-format PDFs without failure
Deduplication
Uses MD5 hashing for page-level deduplication
Prevents redundant storage and improves query efficiency
Noise Reduction
Removes boilerplate text (headers, footers, page numbers)
Filters low-quality chunks based on heuristics
Improves signal-to-noise ratio
Token-Aware Chunking
Uses tokenizer aligned with embedding model
Ensures chunk size stays within token limits
Applies sliding window with overlap to preserve context
Efficient Storage
Stores data in JSONL format
Supports streaming ingestion
Avoids memory bottlenecks for large datasets
Semantic Retrieval
Uses Sentence Transformers for embeddings
Retrieves based on semantic similarity instead of keywords
Grounded Response Generation
Strict prompt engineering to reduce hallucination
Context-aware answer generation
Includes source attribution
Project Structure
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
Data Pipeline
1. Hybrid PDF Extraction

The system first attempts text extraction using PyMuPDF. If no usable text is found, it falls back to OCR.

if not text.strip():
    text = extract_text_with_ocr(page)

This ensures robustness when dealing with scanned or image-based PDFs.

2. Deduplication

Each extracted page is hashed using MD5 to prevent duplicate processing.

text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()

This reduces storage overhead and improves retrieval performance.

3. Noise Filtering

Text is filtered using heuristics to remove low-quality or irrelevant content.

if alpha_chars / len(text) < 0.3:
    return True

This step significantly improves downstream model performance.

4. Token-Aware Chunking

Instead of splitting text by characters, the system uses token-based chunking aligned with the embedding model.

Maintains chunk size within limits
Uses overlap to preserve context across chunks
JSONL Data Format

Each chunk is stored as a separate JSON object:

{
  "doc_id": "25845916",
  "file": "25845916.pdf",
  "category": "misc",
  "page_span": [1, 1],
  "text": "...",
  "chunk_hash": "abc123"
}
Advantages of JSONL
Memory-efficient streaming
Flexible schema for metadata
Scales well with large datasets
Embedding Layer

The system uses Sentence Transformers:

Model: multi-qa-MiniLM-L6-cos-v1
Converts text into dense vector representations
self.model.encode(text)

These embeddings enable semantic similarity search.

Vector Database

ChromaDB is used for storing and retrieving embeddings.

Key features:

Persistent local storage
Automatic embedding integration
Fault recovery for schema inconsistencies
RAG Pipeline
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
Prompt Engineering

The system enforces strict instructions:

You are an expert in architecture research.
Use only the provided excerpts to answer.

This ensures:

Reduced hallucination
Fact-based responses
Traceability
Performance Optimizations
Model Pre-Warming
Sends a dummy request at startup
Eliminates cold-start latency
Context Truncation
Limits input size to LLM
Reduces response time
Prevents context overflow
API Layer
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
Features
Input validation using Pydantic
Structured responses
Proper error handling
CORS enabled
CLI Interface

Run queries directly from the terminal:

python main.py --query "fire codes"
Available Commands
Command	Description
--init	Initialize database
--query	Run single query
--interactive	Start interactive mode
Dependencies

Core libraries used:

transformers
sentence-transformers
chromadb
fastapi
pymupdf
pytesseract
torch
Design Decisions
Local Models
Ensures data privacy
No external API cost
Works offline
FastAPI
High performance for async workloads
Built-in documentation
Suitable for ML APIs
Sentence Transformers
Optimized for semantic search
Better performance for Q&A retrieval tasks
Challenges Addressed
Problem	Solution
Scanned PDFs	OCR fallback
Duplicate pages	Hash-based deduplication
Context loss	Sliding window chunking
Hallucination	Strict prompt constraints
High latency	Pre-warming and truncation
Future Improvements
Frontend integration (React / Next.js)
Hybrid search (BM25 + vector search)
Re-ranking models
Cloud deployment
Authentication and user management
Setup and Usage
# Install dependencies
python requirements.py

# Initialize database
python main.py --init

# Start API server
uvicorn api:app --reload

# Example query
curl -X POST http://localhost:8000/query
Summary

This project demonstrates a full RAG pipeline that ingests unstructured PDF data, transforms it into semantic embeddings, retrieves relevant context, and generates grounded responses using a local language model.
