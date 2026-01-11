from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database import Base, engine
import app.models
from app.routers import auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="E-commerce API",
    version="0.2.0",
    lifespan=lifespan
)

# ⬅️ Router só DEPOIS de criar o app
app.include_router(auth.router)


@app.get("/")
def health_check():
    return {"status": "API online"}



