import ollama
import time
from typing import List, Dict, Any
from config import config
from database import ResearchPaperDatabase

class RAGPipeline:
    def __init__(self):
        self.db = ResearchPaperDatabase()
        self.ollama_client = ollama.Client(host=config.OLLAMA_BASE_URL)
        # Optionally pre-warm Ollama to load model into memory and reduce first-call latency
        if getattr(config, 'PREWARM_OLLAMA', False):
            try:
                print("[RAG] Pre-warming Ollama model (this may take a while)...")
                t0 = time.time()
                # small warm-up prompt
                self.ollama_client.chat(
                    model=config.OLLAMA_MODEL,
                    messages=[{"role": "user", "content": "Hello"}]
                )
                print(f"[RAG] Pre-warm completed in {time.time() - t0:.2f}s")
            except Exception as e:
                print(f"[RAG] Pre-warm failed: {e}")
    
    def generate_response(self, query: str, context: List[str]) -> str:
        """Generate response using Ollama with retrieved context"""
        
        # Prepare the context (truncate long documents to limit prompt size)
        truncated = [doc[:config.TRUNCATE_DOC_CHARS] for doc in context]
        context_text = "\n\n".join([
            f"Reference {i+1}:\n{doc}" for i, doc in enumerate(truncated)
        ])

        # Shorter system prompt to reduce prompt size and latency
        system_prompt = (
            "You are an expert in architecture research. Use only the provided excerpts to answer. "
            "Keep answers factual, cite references where possible, and be concise."
        )

        # User prompt with context (kept compact)
        user_prompt = f"Based on the excerpts below, answer: {query}\n\nContext:\n{context_text}\n\nProvide a concise, referenced answer."

        try:
            print("[RAG] Sending prompt to Ollama... (this may take a while)")
            t0 = time.time()
            response = self.ollama_client.chat(
                model=config.OLLAMA_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            elapsed = time.time() - t0
            print(f"[RAG] Ollama generation completed in {elapsed:.2f}s")
            return response['message']['content']

        except Exception as e:
            elapsed = time.time() - t0 if 't0' in locals() else 0
            print(f"[RAG] Ollama call failed after {elapsed:.2f}s: {e}")
            return f"Error generating response: {str(e)}"
    
    def query(self, user_query: str, n_results: int = config.TOP_K_RESULTS) -> Dict[str, Any]:
        """Complete RAG pipeline: retrieve and generate"""
        # Step 1: Query the database
        print("[RAG] Searching for relevant research papers...")
        t0 = time.time()
        results = self.db.query_documents(user_query, n_results)
        retrieval_time = time.time() - t0
        print(f"[RAG] Retrieval completed in {retrieval_time:.2f}s")
        
        if not results or not results['documents']:
            return {
                "answer": "No relevant research papers found for your query.",
                "sources": [],
                "context": []
            }
        
        # Extract retrieved documents
        retrieved_docs = results['documents'][0]
        metadatas = results['metadatas'][0]
        distances = results['distances'][0] if 'distances' in results else [0] * len(metadatas)
        
        # Step 2: Generate response
        print("[RAG] Generating comprehensive answer...")
        t0 = time.time()
        answer = self.generate_response(user_query, retrieved_docs)
        generation_time = time.time() - t0
        print(f"[RAG] Total generation call time: {generation_time:.2f}s")
        
        # Prepare source information
        sources = []
        for i, (metadata, distance) in enumerate(zip(metadatas, distances)):
            source_info = {
                "source_id": i+1,
                "title": metadata.get('title', 'Unknown Title'),
                "authors": metadata.get('authors', []),
                "year": metadata.get('year', 'Unknown'),
                "confidence": f"{1 - distance:.3f}" if distance is not None else "N/A"
            }
            sources.append(source_info)
        
        return {
            "answer": answer,
            "sources": sources,
            "context": retrieved_docs,
            "query": user_query
        }
    
    def initialize_database(self, jsonl_files: List[str]):
        """Initialize the database with research papers"""
        print("Initializing database with research papers...")
        self.db.add_documents_from_jsonl(jsonl_files)
        self.db.persist()
        print("Database initialization complete!")