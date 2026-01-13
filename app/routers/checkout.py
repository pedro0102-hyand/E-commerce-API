from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.order import Order
from app.models.product import Product
from app.models.order_status import OrderStatus
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/checkout", tags=["Checkout"])

@router.post("/")
def checkout(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # 1. Busca o carrinho ativo (status CART)
    order = db.query(Order).filter(
        Order.user_id == current_user.id,
        Order.status == OrderStatus.CART
    ).first()

    if not order or not order.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Carrinho vazio ou não encontrado"
        )

    # 2. Validação de Estoque (Safety Check)
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Estoque insuficiente para o produto: {product.name}"
            )

    # 3. Finalizar checkout
    # Alteramos o status para aguardar o pagamento (Fase 7)
    order.status = OrderStatus.PENDING_PAYMENT
    
    db.commit()
    db.refresh(order)

    return {
        "message": "Checkout realizado com sucesso! Aguardando pagamento.",
        "order_id": order.id,
        "total": order.total,
        "status": order.status
    }