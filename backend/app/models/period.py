from sqlalchemy import Column, Integer, String, Date
from app.core.database import Base

class Period(Base):
    __tablename__ = "periods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)        # VD: Quý 1/2024
    code = Column(String(50), unique=True, nullable=False)  # VD: Q1-2024
    start_date = Column(Date)
    end_date = Column(Date)
