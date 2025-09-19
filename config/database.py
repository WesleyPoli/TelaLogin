from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from config.settings import settings

# Configuração do banco de dados PostgreSQL
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency para obter sessão do banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Cria todas as tabelas do banco de dados"""
    Base.metadata.create_all(bind=engine)
