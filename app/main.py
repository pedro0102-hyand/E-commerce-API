from fastapi import FastAPI
from contextlib import asynccontextmanager
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.database import Base, engine
import app.models
from app.routers import auth, products, cart, checkout, payments, orders
from app.utils import limiter  # Importando o limiter isolado

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cria as tabelas no banco de dados ao iniciar
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="E-commerce API",
    version="0.9.0", 
    lifespan=lifespan
)

# Configuração do Rate Limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Registro dos Routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(checkout.router)
app.include_router(payments.router)
app.include_router(orders.router)

@app.get("/")
def health_check():
    return {"status": "API online"}



