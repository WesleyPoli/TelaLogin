from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from models.user import User
from config.database import get_db
from schemas.user_schemas import UserResponse, UserUpdate

class UserController:
    """Controller responsável pelas operações de usuário"""
    
    async def get_user_by_id(self, user_id: int, db: Session = Depends(get_db)) -> UserResponse:
        """Busca usuário por ID"""
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuário não encontrado"
                )
            
            return UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )
    
    async def get_user_by_username(self, username: str, db: Session = Depends(get_db)) -> UserResponse:
        """Busca usuário por username"""
        try:
            user = db.query(User).filter(User.username == username).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuário não encontrado"
                )
            
            return UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )
    
    async def get_all_users(self, db: Session = Depends(get_db)) -> List[UserResponse]:
        """Lista todos os usuários"""
        try:
            users = db.query(User).all()
            return [
                UserResponse(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    is_active=user.is_active,
                    created_at=user.created_at,
                    updated_at=user.updated_at
                )
                for user in users
            ]
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )
    
    async def update_user(self, user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)) -> UserResponse:
        """Atualiza dados do usuário"""
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuário não encontrado"
                )
            
            # Atualizar campos fornecidos
            if user_update.email is not None:
                user.email = user_update.email
            if user_update.is_active is not None:
                user.is_active = user_update.is_active
            
            db.commit()
            db.refresh(user)
            
            return UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )
    
    async def delete_user(self, user_id: int, db: Session = Depends(get_db)) -> dict:
        """Remove usuário (soft delete)"""
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuário não encontrado"
                )
            
            user.is_active = False
            db.commit()
            
            return {"message": "Usuário removido com sucesso"}
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )
