from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
import json

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
    db_feature = create_feature(
        session, geometry=str(feature.geometry), type_=feature.type
    )
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
def delete_feature(feature_id: int, session: Session = Depends(get_session)):
    ok = delete_feature_by_id(session, feature_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Feature not found")
    return {"ok": True}


@router.get("/stats")
def get_stats(session: Session = Depends(get_session)):
    stats = get_feature_stats(session)
    return stats
