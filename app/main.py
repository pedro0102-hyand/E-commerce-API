from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import Base, engine
import app.models  

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="E-commerce API",
    version="0.2.0",
    lifespan=lifespan
)

@app.get("/")
def health_check():
    return {"status": "API online"}


