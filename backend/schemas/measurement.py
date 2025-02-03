from datetime import datetime
from pydantic import BaseModel

class MeasurementRequest(BaseModel):
    device_id: str
    time_ms: int
    value: float

class MeasurementResponse(BaseModel):
    id: int
    device_id: str
    time_ms: int
    timestamp: datetime
    value: float

    class Config:
        orm_mode = True
