from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.indicator import Indicator
from app.schemas.indicator import IndicatorCreate, IndicatorOut
from app.core.database import SessionLocal

router = APIRouter(prefix="/indicators", tags=["Chỉ số"])

# Dependency: lấy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=IndicatorOut)
def create_indicator(indicator: IndicatorCreate, db: Session = Depends(get_db)):
    db_indicator = Indicator(**indicator.dict())
    db.add(db_indicator)
    db.commit()
    db.refresh(db_indicator)
    return db_indicator

@router.get("/", response_model=list[IndicatorOut])
def list_indicators(db: Session = Depends(get_db)):
    return db.query(Indicator).all()
