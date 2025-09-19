from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Optional

from models.user import User
from config.database import get_db
from config.settings import settings
from services.auth_service import AuthService
from schemas.auth_schemas import UserLogin, Token, UserCreate

class AuthController:
    """Controller responsável pela autenticação"""
    
    def __init__(self):
        self.auth_service = AuthService()
    
    async def register(self, user_data: UserCreate, db: Session = Depends(get_db)) -> dict:
        """Registra um novo usuário"""
        try:
            # Verificar se usuário já existe
            existing_user = db.query(User).filter(
                (User.username == user_data.username) | (User.email == user_data.email)
            ).first()
            
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username ou email já cadastrado"
                )
            
            # Criar novo usuário
            user = self.auth_service.create_user(user_data, db)
            
            return {
                "message": "Usuário criado com sucesso",
                "user_id": user.id,
                "username": user.username
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )
    
    async def login(self, user_credentials: UserLogin, db: Session = Depends(get_db)) -> Token:
        """Autentica usuário e retorna token"""
        try:
            # Buscar usuário no banco
            user = db.query(User).filter(User.username == user_credentials.username).first()
            
            if not user or not self.auth_service.verify_password(user_credentials.password, user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciais inválidas",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            if not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Usuário inativo"
                )
            
            # Criar token de acesso
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = self.auth_service.create_access_token(
                data={"sub": user.username}, expires_delta=access_token_expires
            )
            
            return Token(access_token=access_token, token_type="bearer")
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )
    
    async def verify_token(self, token: str) -> Optional[str]:
        """Verifica e decodifica o token JWT"""
        return self.auth_service.verify_token(token)
