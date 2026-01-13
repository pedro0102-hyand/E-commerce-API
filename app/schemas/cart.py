from pydantic import BaseModel, Field

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0, description="A quantidade deve ser maior que zero")