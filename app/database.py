from sqlmodel import create_engine, Session, select
from app.models import Feature
from typing import Dict, Sequence

DATABASE_URL = "sqlite:///./features.db"  # для задания и так пойдёт ;)


engine = create_engine(DATABASE_URL, echo=True)


def create_feature(session: Session, geometry: str, type_: str) -> Feature:
    db_feature = Feature(geometry=geometry, type=type_)
    session.add(db_feature)
    session.commit()
    session.refresh(db_feature)
    return db_feature


def get_all_features(session: Session) -> Sequence[Feature]:
    return session.exec(select(Feature)).all()


def delete_feature_by_id(session: Session, feature_id: str) -> bool:
    feature = session.get(Feature, feature_id)
    if not feature:
        return False
    session.delete(feature)
    session.commit()
    return True


def get_feature_stats(session: Session) -> Dict[str, int]:
    features = session.exec(select(Feature)).all()
    stats = {"points": 0, "lines": 0, "polygons": 0}
    for f in features:
        if f.type.lower() == "point":
            stats["points"] += 1
        elif f.type.lower() == "linestring":
            stats["lines"] += 1
        elif f.type.lower() == "polygon":
            stats["polygons"] += 1
    return stats
