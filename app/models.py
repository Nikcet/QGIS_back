from typing import Optional
from sqlmodel import SQLModel, Field
from shortuuid import uuid


class Feature(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: uuid(), primary_key=True)
    geometry: str  # GeoJSON как строка
    type: str  # Point, LineString, Polygon
