from pydantic import BaseModel
from datetime import datetime
from typing import List
from app.models.order_status import OrderStatus

# define como cada produto deve aparecer como pedido
class OrderItemResponse(BaseModel):

    product_id : int
    quantity: int
    unit_price: float

    class Config:

        from_attributes = True

class OrderResponse(BaseModel):

    id: int
    status: OrderStatus
    total: float
    created_at : datetime
    items: List[OrderItemResponse]

    class Config:

        from_attributes = True