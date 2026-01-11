from enum import Enum

class OrderStatus(str, Enum):
    CART = "cart"
    PENDING_PAYMENT = "pending_payment"
    PAID = "paid"
    CANCELLED = "cancelled"
