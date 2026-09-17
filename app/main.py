from fastapi import FastAPI

app = FastAPI(
    title="Enterprise RAG Assistant",
    description="Enterprise RAG system with RBAC guardrails, evaluation, and monitoring.",
    version="0.1.0"
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service":"enterprise-rag-assistant",
    }