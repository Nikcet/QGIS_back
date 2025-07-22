from typing import Optional
from sqlmodel import SQLModel, Field

class Feature(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    geometry: str  # GeoJSON как строка
    type: str     # Point, LineString, Polygon
