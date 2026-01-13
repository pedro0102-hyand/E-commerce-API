from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.order import Order
from app.auth.dependencies import get_current_user, get_current_admin_user
from app.schemas.order import OrderResponse

router = APIRouter(prefix="/orders", tags=["Orders"])

# 1. LISTAR PEDIDOS DO PRÓPRIO UTILIZADOR (Cliente)
@router.get("/me", response_model=List[OrderResponse])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Retorna todos os pedidos, exceto o carrinho atual, ou todos se preferires
    return db.query(Order).filter(Order.user_id == current_user.id).all()

# 2. DETALHAR UM PEDIDO ESPECÍFICO (Cliente)
@router.get("/{order_id}", response_model=OrderResponse)
def get_order_detail(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    order = db.query(Order).filter(
        Order.id == order_id, 
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return order

# 3. LISTAR TODOS OS PEDIDOS (Admin Only)
@router.get("/admin/all", response_model=List[OrderResponse])
def get_all_orders_admin(
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin_user)
):
    return db.query(Order).all()