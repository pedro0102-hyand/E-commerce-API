from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from app.database import get_db
from app.models.order import Order
from app.models.product import Product
from app.models.order_status import OrderStatus
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/{order_id}")
def process_payment(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # 1. Procurar o pedido pendente do utilizador
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id,
        Order.status == OrderStatus.PENDING_PAYMENT
    ).first()

    if not order:
        raise HTTPException(
            status_code=404, 
            detail="Pedido pendente não encontrado."
        )

    # 2. Simulação de Pagamento e Atualização de Stock
    # Usamos um loop para baixar o stock de cada item
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        
        # Re-validação de segurança antes de baixar o stock
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Infelizmente o produto {product.name} esgotou durante o processo."
            )
        
        # Redução efetiva do stock
        product.stock -= item.quantity

    # 3. Atualizar status do pedido
    order.status = OrderStatus.PAID
    # Nota: Podes adicionar um campo 'payment_id' ou 'paid_at' no teu modelo Order se quiseres mais detalhe
    
    db.commit()
    
    return {
        "message": "Pagamento confirmado com sucesso!",
        "order_id": order.id,
        "payment_reference": str(uuid.uuid4()), # ID fake de transação
        "new_status": order.status
    }