from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.dependencies import get_current_admin_user

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/")
def create_product(
    name: str,
    price: float,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin_user),
):
    return {"message": "Produto criado (admin)"}
