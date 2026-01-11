from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.auth.security import verify_password, get_password_hash
from app.auth.jwt import create_access_token
from app.schemas.user import UserCreate, UserResponse 

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
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
    
    # 2. Cria o novo usuário (is_admin é False por padrão no modelo)
    new_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Gera o token de acesso (JWT) para o usuário.
    """
    # Busca o usuário pelo e-mail (que o OAuth2 chama de username)
    user = db.query(User).filter(User.email == form_data.username).first()

    # Valida se o usuário existe e se a senha está correta
    if not user or not verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos",
        )

    # Cria o token JWT com o e-mail do usuário no campo 'sub'
    access_token = create_access_token(
        data={"sub": user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
