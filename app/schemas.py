from pydantic import BaseModel


class FeatureCreate(BaseModel):
    geometry: dict  # GeoJSON
    type: str  # Point, LineString, Polygon
