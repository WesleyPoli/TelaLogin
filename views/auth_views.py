from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from config.database import get_db
from controllers.auth_controller import AuthController
from schemas.auth_schemas import UserCreate, UserLogin, Token

# Criar router para autenticação
auth_router = APIRouter(prefix="/auth", tags=["autenticação"])

# Instanciar controller
auth_controller = AuthController()

@auth_router.get("/", response_class=HTMLResponse)
async def login_page():
    """Serve a página de login"""
    with open("static/login.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@auth_router.post("/register", response_model=dict)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Registra um novo usuário"""
    return await auth_controller.register(user, db)

@auth_router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Autentica usuário e retorna token"""
    return await auth_controller.login(user_credentials, db)

@auth_router.get("/protected")
async def protected_route():
    """Rota protegida para teste"""
    return {"message": "Esta é uma rota protegida! Você está autenticado."}
