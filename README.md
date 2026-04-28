Architechs-RAG: Neural-Architecture Search with Zero-Hallucination GroundingArchitechs-RAG is a Retrieval-Augmented Generation (RAG) pipeline engineered for architectural research. It addresses the challenge of LLM hallucinations by enforcing a strict data-to-answer contract through multi-stage ingestion, semantic space mapping, and verifiable source provenance.  The Problem: Addressing LLM HallucinationsStandard AI models often suffer from hallucinations, confidently inventing building codes, citing non-existent materials, or losing context in massive PDFs. This project implements a three-layer defense strategy:  Strict Prompt Grounding: The LLM is programmatically restricted to using only the provided excerpts to answer queries .  Source Provenance: Every response includes metadata, such as file name, page number, and chunk hash, to allow for immediate human verification .  Signal-to-Noise Optimization: A custom regex gauntlet strips boilerplate text like repeated copyrights and formatting artifacts, ensuring the LLM only processes high-density factual "signal" .  Architectural FlowCode snippetgraph TD
    subgraph "1. Ingestion Pipeline"
    A[Raw PDFs & Blueprints] --> B{Hybrid Extraction}
    B -->|Text-Based| C[PyMuPDF]
    B -->|Scanned/Image| D[Tesseract OCR]
    C --> E[MD5 De-duplication]
    D --> E
    E --> F[Quality Filtering/Regex]
    F --> G[Token-Aware Sliding Window]
    end

    subgraph "2. Vector Space"
    G --> H[SentenceTransformer Embeddings]
    H --> I[(ChromaDB)]
    end

    subgraph "3. Interface Layer"
    J[User Query] --> K[Vector Similarity Search]
    I --> K
    K --> L[Grounded Context Injection]
    L --> M[Ollama LLM]
    M --> N[Verified Answer + Citations]
    end
Technical Implementation1. Robust Data IngestionHybrid OCR Fallback: The pipeline first attempts lightweight extraction with PyMuPDF but triggers Tesseract OCR if a page is a scanned image or blueprint .  Deduplication: The system implements MD5 hashing on extracted text . If a duplicate page is found, the system skips it in $O(1)$ time to prevent database bloating.  2. High-Precision RetrievalToken-Aware Sliding Window: Rather than using naive character counts, the system uses the AutoTokenizer from the embedding model to ensure no chunk exceeds the strict 512-token limit .  Context Bridges: A 60-token overlap between chunks ensures that concepts spanning across page breaks are preserved.  3. Performance and StabilityOllama Pre-Warming: To eliminate cold-start latency, the system fires a silent query on startup to load the LLM weights into RAM before user interaction .  JSONL Streaming: The dataset is structured in JSON Lines, allowing the system to process massive files line-by-line without hitting Out-of-Memory (OOM) errors .  Auto-Recovery Database: A custom wrapper detects ChromaDB schema mismatches and automatically rebuilds the local vector store if corruption is detected .  Evaluation and StrategyStrategyImplementationBenefitData IntegrityMD5 Hashing and Boilerplate StrippingRemoves redundant noise and "Garbage In" effects.  Model Choicemulti-qa-MiniLM (Specific for Q&A)Superior to generic similarity models for semantic search.  DevOpsPinned Dependency ScriptPrevents breaking changes in rapidly evolving AI libraries .  API LogicFastAPI Asynchronous RoutingEfficiently handles I/O-bound operations like database queries and token generation.  Getting StartedInstallationThe project uses a custom script for programmatic, version-pinned installation:Bashpython requirements.py
  UsageInteractive CLI:Bashpython main.py --interactive
  API Deployment:Bashuvicorn api:app --reload
  Engineering NoteFastAPI was selected for this project because RAG systems are primarily I/O-bound. While the system waits for the vector database or the LLM to generate tokens, FastAPI handles other requests asynchronously, providing better scalability for a production frontend than traditional frameworks.  
