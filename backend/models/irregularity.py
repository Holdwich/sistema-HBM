from sqlalchemy import Column, Integer, String, DateTime
from core.database import Base

class Irregularity(Base):
    __tablename__ = "irregularities"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(50), index=True)
    start_timestamp = Column(DateTime)
    end_timestamp = Column(DateTime, nullable=True)
