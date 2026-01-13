from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel): # classe PAI, defini como os produtos serao no sistema

    name: str
    description: str
    price: float
    stock: int

class ProductCreate(ProductBase):
    pass 

class ProductUpdate(BaseModel): # permitir atualizacao sobre o produto

    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True