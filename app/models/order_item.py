from sqlalchemy import Integer, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class OrderItem(Base):

    __tablename__ = "order_items"

    # Cria o ID, é incrementado automaticamente no DB
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # armazena o ID do pedido
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))

    # armazena o ID do produto
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    quantity: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[float] = mapped_column(Float)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="items")
