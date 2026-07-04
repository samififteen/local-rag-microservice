import os
import chromadb
from chromadb.utils import embedding_functions
from typing import List

class VectorStoreService:
    def __init__(self):
        # Retrieve the API key from the environment
        api_key = os.getenv("OPENAI_API_KEY")
        
        # Setup a local folder to store our vector database on disk
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db_data")
        
        # Configure ChromaDB to automatically use OpenAI to turn text into embeddings
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=api_key,
            model_name="text-embedding-3-small"
        )
        
        # Get or create our vector collection database table
        self.collection = self.chroma_client.get_or_create_collection(
            name="rag_collection",
            embedding_function=self.embedding_function
        )

    def chunk_text(self, text: str, chunk_size: int = 300, overlap: int = 30) -> List[str]:
        """Splits a long string into smaller, overlapping word chunks."""
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        return chunks

    def add_document(self, text: str, source_name: str) -> int:
        """Chunks a document and saves it directly into ChromaDB."""
        chunks = self.chunk_text(text)
        
        # Create a unique ID for every single text chunk
        ids = [f"{source_name}_{i}" for i in range(len(chunks))]
        metadatas = [{"source": source_name} for _ in chunks]
        
        self.collection.add(
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )
        return len(chunks)

    def find_relevant_context(self, query: str, top_k: int) -> List[str]:
        """Searches the database for chunks matching the meaning of the query."""
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        # Pull out and return the raw text chunks
        if results and results.get("documents"):
            return results["documents"][0]
        return []

# Create a singleton instance to use across our application
vector_store_service = VectorStoreService()