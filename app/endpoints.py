import json
import os

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session, select

from app import logger
from app.models import Feature as FeatureModel
from app.dependencies import get_session
from app.schemas import FeatureCreate
from app.database import (
    create_feature,
    get_all_features,
    delete_feature_by_id,
    get_feature_stats,
)

router = APIRouter()


@router.post("/features")
def add_feature(feature: FeatureCreate, session: Session = Depends(get_session)):
    existing = session.exec(
        select(FeatureModel).where(FeatureModel.geometry == str(feature.geometry))
    ).first()
    if existing:
        return

    if not feature.geometry:
        raise HTTPException(status_code=400, detail="Geometry is required")
    try:
        feature_json = json.loads(feature.geometry)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid geometry JSON")
    type_ = feature_json.get("type")
    if not type_:
        raise HTTPException(status_code=400, detail="Type is required in geometry")

    db_feature = create_feature(session, geometry=str(feature.geometry), type_=type_)

    logger.info(f"Post db feature: {db_feature}")
    return {"id": db_feature.id}


@router.get("/features")
def get_features(session: Session = Depends(get_session)):
    features = get_all_features(session)
    feature_collection = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "id": f.id,
                "geometry": json.loads(f.geometry),
                "properties": {"type": f.type},
            }
            for f in features
        ],
    }
    return feature_collection


@router.delete("/features/{feature_id}")
def delete_feature(feature_id: str, session: Session = Depends(get_session)):
    ok = delete_feature_by_id(session, feature_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Feature not found")
    return {"ok": True}


@router.get("/stats")
def get_stats(session: Session = Depends(get_session)):
    stats = get_feature_stats(session)
    return stats


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, session: Session = Depends(get_session)):
    templates = Jinja2Templates(
        directory=os.path.join(os.path.dirname(__file__), "templates")
    )
    stats = get_feature_stats(session)
    features = get_all_features(session)[-10:]  # последние 10 объектов
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "stats": stats, "features": features}
    )
