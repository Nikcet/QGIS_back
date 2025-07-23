from pydantic import BaseModel


class FeatureCreate(BaseModel):
    geometry: str  # GeoJSON
    type: str  # Point, LineString, Polygon
