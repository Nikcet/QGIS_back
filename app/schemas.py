from pydantic import BaseModel


class FeatureCreate(BaseModel):
    geometry: str  # GeoJSON
