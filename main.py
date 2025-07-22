from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from sqlmodel import Session

from app import logger
from app.endpoints import router
from app.database import engine, get_feature_stats, get_all_features
from app.dependencies import get_session
from app.models import SQLModel
import os

app = FastAPI()

app.include_router(router)

templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), "templates")
)


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, session: Session = Depends(get_session)):
    stats = get_feature_stats(session)
    features = get_all_features(session)[-10:]  # последние 10 объектов
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "stats": stats, "features": features}
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.success("Server is startup...")
    SQLModel.metadata.create_all(engine)
    yield
    logger.warning("Servir is shutting down...")


app = FastAPI(lifespan=lifespan)
