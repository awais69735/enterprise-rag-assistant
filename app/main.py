from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from jose import JWTError

from app.auth.authentication import authenticate_user
from app.auth.jwt import create_access_token, decode_access_token
from app.rag.pipeline import RAGPipeline

from app.guardrails.manager import GuardrailManager
from app.guardrails.audit import log_guardrails_event

app = FastAPI(
    title="Enterprise RAG Assistant",
    description="Enterprise RAG system with RBAC guardrails, evaluation, and monitoring.",
    version="0.1.0"
)

security= HTTPBearer()

rag = RAGPipeline()

guardrails = GuardrailManager()

class LoginRequest(BaseModel):
    username: str
    password: str

class ChatRequest(BaseModel):
    question: str

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service":"enterprise-rag-assistant",
    }

@app.post("/auth/login")
def login(request: LoginRequest):
    user= authenticate_user(
        username= request.username,
        password= request.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    access_token= create_access_token(
        username=user["username"],
        role=user['role']
    )

    return {
        "access_token": access_token,
        "token_type":"bearer",
        "user":user
    }


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    try:
        payload = decode_access_token(token)

        username= payload.get("sub")
        role = payload.get("role")

        if not username or not role:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication token"
            )

        return {
            "username": username,
            "role": role
        }

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired authentication token"
        )

@app.get("/auth/me")
def get_me(current_user:dict = Depends(get_current_user)):
    return current_user


@app.post("/chat")
def chat(
    request: ChatRequest,
    current_user: dict= Depends(get_current_user)
):

    validation = guardrails.validate_question(request.question)

    if not validation["allowed"]:
        log_guardrails_event(
            username=current_user["username"],
            role=current_user["role"],
            action="question_validation",
            reason=validation["reason"],
            details=validation["details"]
        )
        return {
            "username":current_user["username"],
            "role":current_user["role"],
            "question": request.question,
            "answer":"This question cannot be processed.",
            "blocked":True,
            "reason":validation["reason"],
            "details": validation["details"],
            "sources":[]
        }
    
    result= rag.answer(
        question= request.question,
        role= current_user["role"]
    )
    response_validation = guardrails.validate_response(
        result["answer"]
    )

    if not response_validation["allowed"]:
        log_guardrails_event(
            username=current_user["username"],
            role=current_user["role"],
            action="response_validation",
            reason= response_validation["reason"],
            details=response_validation["details"]
        )
        return {
            "username":current_user["username"],
            "role":current_user["role"],
            "question":request.question,
            "answer":"The generated response contains sensitive information cannot be returned.",
            "blocked": True,
            "reason": response_validation["reason"],
            "details": response_validation["details"],
            "sources": []
        }

    return {
        "username":current_user["username"],
        "role": current_user["role"],
        "question": request.question,
        "answer": result["answer"],
        "blocked":False,
        "reason":None,
        "details":[],
        "sources": result["sources"]
    }