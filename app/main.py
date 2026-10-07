from fastapi import FastAPI
from pydantic import BaseModel
from rag.rag_service import generate_rag_response
app = FastAPI(
    title="AI Customer Support Agent",
    description="An AI-powered customer support agent that can handle customer queries and provide assistance.",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    message: str


class Source(BaseModel):
    source: str
    chunk_id: int


class ChatResponse(BaseModel):
    response: str
    sources: list[Source] = []


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    response = generate_rag_response(request.message)

    return {
        "response": response["answer"],
        "sources": response["sources"]
    }