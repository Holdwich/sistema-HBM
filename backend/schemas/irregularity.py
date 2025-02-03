from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class IrregularityResponse(BaseModel):
    id: int
    device_id: str
    start_timestamp: datetime
    end_timestamp: Optional[datetime] = None

    class Config:
        orm_mode = True
