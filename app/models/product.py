from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Product(Base):
    
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(String, index=True)

    description: Mapped[str] = mapped_column(String)

    price: Mapped[float] = mapped_column(Float)

    stock: Mapped[int] = mapped_column(Integer)

    items = relationship("OrderItem", back_populates="product")
