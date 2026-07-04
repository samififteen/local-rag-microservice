from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

# Crucial: Load the environment variables from the .env file before anything else imports
load_dotenv()

from app.schemas import IngestRequest, IngestResponse, QueryRequest, QueryResponse
from app.services.vector_store import vector_store_service
from app.services.llm import llm_service

app = FastAPI(
    title="Simple RAG API",
    description="A clean API to ingest text and query it using context-augmented generation.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "The RAG API is live. Go to /docs to test your endpoints!"}

@app.post("/ingest", response_model=IngestResponse)
async def ingest(payload: IngestRequest):
    try:
        num_chunks = vector_store_service.add_document(
            text=payload.text, 
            source_name=payload.source_name
        )
        return IngestResponse(status="success", chunks_indexed=num_chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference Ingestion Error: {str(e)}")

@app.post("/query", response_model=QueryResponse)
async def query(payload: QueryRequest):
    try:
        # 1. Search the local vector database for matching text context
        matched_text_chunks = vector_store_service.find_relevant_context(
            query=payload.question, 
            top_k=payload.top_k
        )
        
        # 2. Feed that context alongside the question to the LLM
        ai_response = llm_service.generate_answer(
            question=payload.question, 
            contexts=matched_text_chunks
        )
        
        return QueryResponse(
            question=payload.question,
            answer=ai_response,
            sources_used=matched_text_chunks
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query Pipeline Error: {str(e)}")