from fastapi import FastAPI
from contextlib import asynccontextmanager

from app import logger
from app.endpoints import router
from app.database import engine
from app.models import SQLModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.success("Server is startup...")
    SQLModel.metadata.create_all(engine)
    yield
    logger.warning("Servir is shutting down...")

app = FastAPI(lifespan=lifespan)



app.include_router(router)


