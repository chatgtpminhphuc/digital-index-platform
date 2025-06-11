from sqlalchemy import Column, Integer, Float, ForeignKey
from app.core.database import Base

class DataEntry(Base):
    __tablename__ = "data_entries"

    id = Column(Integer, primary_key=True, index=True)
    indicator_id = Column(Integer, ForeignKey("indicators.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    period_id = Column(Integer, ForeignKey("periods.id"), nullable=False)
    value = Column(Float, nullable=True)
