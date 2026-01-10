from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import Base, engine

# Garante a inicializacao do banco assim que o servidor rodar
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown (se precisar no futuro)

# Iniciando o FastAPI
app = FastAPI(
    title="E-commerce API",
    version="0.1.0",
    lifespan=lifespan
)

# Checando se a aplicacao funciona
@app.get("/")
def health_check():
    return {"status": "API online"}

