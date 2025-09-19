from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from config.database import get_db
from controllers.user_controller import UserController
from schemas.user_schemas import UserResponse, UserUpdate

# Criar router para usuários
user_router = APIRouter(prefix="/users", tags=["usuários"])

# Instanciar controller
user_controller = UserController()

@user_router.get("/", response_model=List[UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    """Lista todos os usuários"""
    return await user_controller.get_all_users(db)

@user_router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Busca usuário por ID"""
    return await user_controller.get_user_by_id(user_id, db)

@user_router.get("/username/{username}", response_model=UserResponse)
async def get_user_by_username(username: str, db: Session = Depends(get_db)):
    """Busca usuário por username"""
    return await user_controller.get_user_by_username(username, db)

@user_router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """Atualiza dados do usuário"""
    return await user_controller.update_user(user_id, user_update, db)

@user_router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Remove usuário (soft delete)"""
    return await user_controller.delete_user(user_id, db)
