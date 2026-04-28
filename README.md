🧠 RAG-Based Architecture Research Assistant

A production-grade Retrieval-Augmented Generation (RAG) system designed to process architectural PDFs, extract meaningful knowledge, and answer queries using a grounded LLM pipeline.

🚀 Overview

This project builds a complete end-to-end RAG pipeline:

📄 Extracts data from messy PDFs (including scanned ones)
🧹 Cleans and filters noisy architectural text
✂️ Splits data into token-aware chunks
🔢 Converts text into vector embeddings
🗄️ Stores embeddings in ChromaDB
🤖 Uses a local LLM (Ollama) to generate grounded answers
🌐 Exposes everything via a FastAPI backend
🏗️ System Architecture
                ┌───────────────┐
                │   PDF Files   │
                └──────┬────────┘
                       │
                       ▼
        ┌─────────────────────────────┐
        │ Data Cleaning Pipeline      │
        │ (OCR + Dedup + Filtering)  │
        └──────────┬──────────────────┘
                   │
                   ▼
        ┌─────────────────────────────┐
        │ Token-Aware Chunking        │
        │ (Sliding Window + Overlap)  │
        └──────────┬──────────────────┘
                   │
                   ▼
        ┌─────────────────────────────┐
        │ JSONL Dataset               │
        │ (Chunks + Metadata)         │
        └──────────┬──────────────────┘
                   │
                   ▼
        ┌─────────────────────────────┐
        │ Embedding Model             │
        │ (Sentence Transformers)     │
        └──────────┬──────────────────┘
                   │
                   ▼
        ┌─────────────────────────────┐
        │ Vector DB (ChromaDB)        │
        └──────────┬──────────────────┘
                   │
                   ▼
        ┌─────────────────────────────┐
        │ RAG Pipeline                │
        │ (Retrieve + Prompt + LLM)   │
        └──────────┬──────────────────┘
                   │
                   ▼
        ┌─────────────────────────────┐
        │ FastAPI / CLI Interface     │
        └─────────────────────────────┘
⚙️ Features
✅ Fault-Tolerant PDF Processing
Uses PyMuPDF first, falls back to Tesseract OCR
Handles scanned PDFs automatically
Deduplicates pages using MD5 hashing
✅ Noise Reduction
Removes:
Boilerplate text
Page numbers
Formatting artifacts
Improves Signal-to-Noise Ratio (SNR)
✅ Smart Chunking
Token-aware chunking using model tokenizer
Sliding window with overlap
Prevents context loss across chunks
✅ Efficient Storage
Uses JSONL format
Supports streaming ingestion
Avoids memory overflow
✅ Semantic Retrieval
Uses multi-qa-MiniLM embeddings
Retrieves based on meaning, not keywords
✅ Grounded LLM Responses
Strict prompt engineering
Prevents hallucination
Provides source references
📂 Project Structure
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
🔍 Data Pipeline (Step-by-Step)
1️⃣ Hybrid PDF Extraction
Extract text using PyMuPDF
If empty → fallback to OCR
if not text.strip():
    text = extract_text_with_ocr(page)

💡 Why this matters:
Real-world PDFs are messy — this ensures no data loss.

2️⃣ Deduplication
Uses MD5 hashing
text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()

💡 Prevents:

Duplicate storage
Redundant embeddings
Slower queries
3️⃣ Noise Filtering
Removes low-quality text
if alpha_chars / len(text) < 0.3:
    return True

💡 Ensures:

Garbage In = Garbage Out ❌
Clean Data = Accurate AI ✅

4️⃣ Token-Based Chunking

Instead of characters → uses tokens

Chunk A: [------text------]
Chunk B:      [------text------]
Overlap ensures context continuity
🧾 JSONL Data Format

Each line = one chunk

{
  "doc_id": "25845916",
  "file": "25845916.pdf",
  "category": "misc",
  "page_span": [1, 1],
  "text": "...",
  "chunk_hash": "abc123"
}
Why JSONL?
Feature	Benefit
Streaming	Handles large datasets
Flexible	Supports metadata
Memory Efficient	No full load required
🧠 Embedding Layer
Uses Sentence Transformers
Model: multi-qa-MiniLM-L6-cos-v1
self.model.encode(text)
What it does:

Converts text → vector

"building design" → [0.23, -0.91, ...]

💡 Enables semantic search

🗄️ Vector Database (ChromaDB)
Stores embeddings
Supports similarity search
Auto-embeds via wrapper
Bonus Feature:

✔ Auto-recovery if DB breaks

🎯 RAG Pipeline Flow
User Query
   │
   ▼
Convert to Embedding
   │
   ▼
Retrieve Top-K Chunks
   │
   ▼
Inject into Prompt
   │
   ▼
LLM Generates Answer
🧾 Prompt Engineering
You are an expert in architecture research.
Use ONLY the provided excerpts.
Why?
Prevent hallucination
Ensure factual answers
⚡ Performance Optimizations
🚀 Pre-Warming LLM
Sends dummy request at startup
Eliminates cold start delay
✂️ Context Truncation
Prevents token overflow
Reduces latency
🌐 API Layer (FastAPI)
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
Input validation via Pydantic
Clean error handling
CORS enabled
🖥️ CLI Interface

Run directly from terminal:

python main.py --query "fire codes"
Modes
Command	Description
--init	Rebuild DB
--query	Single query
--interactive	Chat mode
📦 Dependencies

Key libraries:

transformers
sentence-transformers
chromadb
fastapi
pymupdf
pytesseract
torch
🧩 Design Decisions
Why Local Models?
✅ No API cost
✅ Data privacy
✅ Offline capability
Why FastAPI?
Async support
High performance
Auto docs (Swagger)
Why Sentence Transformers?
Optimized for semantic search
Better than generic embeddings
⚠️ Challenges Solved
Problem	Solution
Scanned PDFs	OCR fallback
Duplicate pages	Hashing
Context loss	Sliding window
LLM hallucination	Strict prompts
Latency	Pre-warming
🔮 Future Improvements
Add frontend (React / Next.js)
Use hybrid search (BM25 + vector)
Add re-ranking models
Deploy on cloud (AWS/GCP)
Add user authentication
🧑‍💻 How to Run
# Install dependencies
python requirements.py

# Initialize DB
python main.py --init

# Run API
uvicorn api:app --reload

# Query
curl -X POST http://localhost:8000/query
