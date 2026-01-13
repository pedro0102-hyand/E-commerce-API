from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.order_status import OrderStatus
from app.auth.dependencies import get_current_user
from app.schemas.cart import CartItemCreate

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/add")
def add_to_cart(
    item_in: CartItemCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user) # Usuário logado comum
):
    # 1. Busca o produto e valida o estoque
    product = db.query(Product).filter(Product.id == item_in.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    if product.stock < item_in.quantity:
        raise HTTPException(status_code=400, detail="Estoque insuficiente")

    # 2. Busca um carrinho (Order com status CART) ativo do usuário
    cart = db.query(Order).filter(
        Order.user_id == current_user.id,
        Order.status == OrderStatus.CART
    ).first()

    # 3. Se não houver carrinho ativo, cria um novo
    if not cart:
        cart = Order(user_id=current_user.id, status=OrderStatus.CART, total=0.0)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    # 4. Verifica se o produto já está no carrinho para atualizar a quantidade
    existing_item = db.query(OrderItem).filter(
        OrderItem.order_id == cart.id,
        OrderItem.product_id == product.id
    ).first()

    if existing_item:
        existing_item.quantity += item_in.quantity
    else:
        new_item = OrderItem(
            order_id=cart.id,
            product_id=product.id,
            quantity=item_in.quantity,
            unit_price=product.price
        )
        db.add(new_item)

    # 5. Atualiza o total do carrinho
    cart.total += (product.price * item_in.quantity)
    
    db.commit()
    return {"message": f"Produto {product.name} adicionado ao carrinho"}