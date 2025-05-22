# from pydantic import BaseModel, Field
# from typing import Optional
# from datetime import datetime, timezone

# class Ticket(BaseModel):
#     created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # Ensure UTC time
#     name: str
#     address: str
#     uuid: str
#     message: str
#     mobile: Optional[str] = None  # Optional field
#     latitude: str
#     longitude: str
#     status: Optional[int] = 0  # Optional field
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timezone

class GeoJSONPoint(BaseModel):
    type: str = "Point"
    coordinates: List[float]  # [longitude, latitude]

class Ticket(BaseModel):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    name: str
    address: str
    uuid: str
    message: str
    mobile: Optional[str] = None
    location: GeoJSONPoint  # Store as GeoJSON
    status: Optional[int] = 0
