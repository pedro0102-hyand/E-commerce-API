from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import Base, engine
import app.models
from app.routers import auth
from app.routers import products
from app.routers import cart
from app.routers import auth, products, cart, checkout



@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="E-commerce API",
    version="0.2.0",
    lifespan=lifespan
)


app.include_router(auth.router)

app.include_router(products.router)

app.include_router(cart.router)

app.include_router(checkout.router)

@app.get("/")
def health_check():
    return {"status": "API online"}



