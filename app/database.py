from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Endereco do banco de dados
DATABASE_URL = "sqlite:///./data/ecommerce.db"

# Estabelece conexao ao BD
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Define o canal de comunicacao
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

class Base(DeclarativeBase):
    pass
