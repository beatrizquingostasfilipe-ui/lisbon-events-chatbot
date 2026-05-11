# database/database.py
# Configura a ligação à base de dados SQLite (um ficheiro local, sem instalar nada extra)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# SQLite guarda tudo num ficheiro chamado events.db na pasta do projeto
DATABASE_URL = "sqlite:///./events.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # necessário para SQLite com FastAPI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Cria as tabelas na base de dados (se não existirem)."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Gera uma sessão de base de dados (usada pelo FastAPI)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
