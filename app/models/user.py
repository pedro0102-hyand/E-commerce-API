from sqlalchemy import Boolean, Integer, String
# Atributo da classe será mapeado para uma coluna do db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class User(Base):
    
    __tablename__ = "users"

    # ID é mapeado na coluna do DB
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Garante que dois users nao tenham mesmo e-mail
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    # Armazena a senha em formato HASH
    hashed_password: Mapped[str] = mapped_column(String)
    # Boolean que controla permissoes
    is_admin: Mapped[bool] = mapped_column(Boolean, default=True)

    orders = relationship("Order", back_populates="user")
