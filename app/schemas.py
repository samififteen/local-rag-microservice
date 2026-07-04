from pydantic import BaseModel, Field
from typing import List, Optional

class IngestRequest(BaseModel):
    text: str = Field(..., description="The continuous raw text string to index into the knowledge base.")
    source_name: Optional[str] = Field("unknown", description="An optional tracker label like a file name or ID.")

class IngestResponse(BaseModel):
    status: str
    chunks_indexed: int

class QueryRequest(BaseModel):
    question: str = Field(..., description="The query or question you want to ask.")
    top_k: int = Field(default=3, description="How many relevant text fragments to fetch as context.")

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources_used: List[str]