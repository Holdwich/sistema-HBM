from sqlalchemy import Column, Integer, Float, String, DateTime, func
from core.database import Base

class Measurement(Base):
    __tablename__ = "measurements"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(50), index=True)
    time_ms = Column(Integer)
    timestamp = Column(DateTime, default=func.now())
    value = Column(Float)
