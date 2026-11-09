from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()


# ============================================================
# Schema de login
# ============================================================

class LoginRequest(BaseModel):
    email: str
    password: str


# ============================================================
# Login
# ============================================================

@router.post("/login")
def login(data: LoginRequest):
    return {
        "message": "Login exitoso",
        "token": "demo-token",
        "email": data.email
    }


# ============================================================
# Health check del módulo Auth
# ============================================================

@router.get("/health")
def auth_health():
    return {
        "module": "auth",
        "status": "ok"
    }
