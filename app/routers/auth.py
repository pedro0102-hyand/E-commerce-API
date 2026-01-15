from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.auth.security import verify_password, get_password_hash
from app.auth.jwt import create_access_token
from app.schemas.user import UserCreate, UserResponse 
from app.utils import limiter 

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("3/hour") # Limite rigoroso para evitar criação de contas em massa
def register(
    request: Request, 
    user_in: UserCreate, 
    db: Session = Depends(get_db)
):
    """
    Cria um novo usuário com senha criptografada.
    """
    # 1. Verifica se o e-mail já está em uso
    user_exists = db.query(User).filter(User.email == user_in.email).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este e-mail já está cadastrado."
        )
    
    # 2. Cria o novo usuário
    new_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
@limiter.limit("5/minute") # Limite para evitar ataques de força bruta
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Gera o token de acesso (JWT) para o usuário.
    """
    # Busca o usuário pelo e-mail
    user = db.query(User).filter(User.email == form_data.username).first()

    # Valida se o usuário existe e se a senha está correta
    if not user or not verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos",
        )

    # Cria o token JWT
    access_token = create_access_token(
        data={"sub": user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
