from pydantic import BaseModel, Field

class CartItemCreate(BaseModel): # converte JSON em objeto da classe

    product_id: int
    quantity: int = Field(gt=0, description="A quantidade deve ser maior que zero")