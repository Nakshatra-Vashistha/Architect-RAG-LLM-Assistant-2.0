import os
from pathlib import Path

class Config:
    # Embedding model
    EMBEDDING_MODEL = "multi-qa-MiniLM-L6-cos-v1"
    
    # ChromaDB settings
    COLLECTION_NAME = "architecture_research_papers"

    PERSIST_DIRECTORY = "./chroma_db"       #Here, we need a database file named "chroma_db, (having sub-file => chroma.sqlite3 + metadata) " to establish the database, in order to run the program.
    
    # JSONL files - update these paths to match your actual file locations
    JSONL_FILES = [
        "C:\\Users\\Lenovo\\Documents\\GitHub\\Architect-RAG-LLM-Assistant\\chunks\\building_codes_chunks.jsonl",
        "C:\\Users\\Lenovo\\Documents\\GitHub\\Architect-RAG-LLM-Assistant\\chunks\\case_studies_chunks.jsonl",
        "C:\\Users\\Lenovo\\Documents\\GitHub\\Architect-RAG-LLM-Assistant\\chunks\\material_guide_chunks.jsonl",
        "C:\\Users\\Lenovo\\Documents\\GitHub\\Architect-RAG-LLM-Assistant\\chunks\\misc_chunks.jsonl"
    ]
    
    # Ollama settings
    OLLAMA_MODEL = "llama2"  # or "mistral", "codellama", etc.
    OLLAMA_BASE_URL = "http://localhost:11434"
    
    # RAG settings
    TOP_K_RESULTS = 5
    CHUNK_SIZE = 512
    CHUNK_OVERLAP = 50
    # Generation tuning
    PREWARM_OLLAMA = True  # send a small prompt at startup to load the model into memory
    TRUNCATE_DOC_CHARS = 1200  # max chars per retrieved doc sent to the LLM
    GENERATION_MAX_TOKENS = 256  # target maximum tokens for generation (keeps latency down)

config = Config()