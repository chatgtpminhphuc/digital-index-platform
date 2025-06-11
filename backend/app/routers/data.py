from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.organization import OrganizationCreate, OrganizationOut
from app.schemas.period import PeriodCreate, PeriodOut
from app.schemas.data_entry import DataEntryCreate, DataEntryOut
from app.models.organization import Organization
from app.models.period import Period
from app.models.data_entry import DataEntry
from app.core.database import SessionLocal
from app.schemas.period import PeriodOut
from app.models.period import Period


router = APIRouter(prefix="/data", tags=["Nhập liệu"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/organizations/", response_model=OrganizationOut)
def create_org(org: OrganizationCreate, db: Session = Depends(get_db)):
    new_org = Organization(**org.dict())
    db.add(new_org)
    db.commit()
    db.refresh(new_org)
    return new_org

@router.post("/periods/", response_model=PeriodOut)
def create_period(period: PeriodCreate, db: Session = Depends(get_db)):
    new_period = Period(**period.dict())
    db.add(new_period)
    db.commit()
    db.refresh(new_period)
    return new_period

@router.post("/entries/", response_model=DataEntryOut)
def create_data_entry(entry: DataEntryCreate, db: Session = Depends(get_db)):
    new_entry = DataEntry(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry
@router.get("/entries/", response_model=list[DataEntryOut])
def list_data_entries(db: Session = Depends(get_db)):
    return db.query(DataEntry).all()
@router.get("/debug/")
def debug_all_data(db: Session = Depends(get_db)):
    entries = db.query(DataEntry).all()
    return [
        {
            "entry_id": e.id,
            "org_id": e.organization_id,
            "period_id": e.period_id,
            "indicator_id": e.indicator_id,
            "value": e.value
        }
        for e in entries
    ]
@router.get("/periods/", response_model=list[PeriodOut])
def list_periods(db: Session = Depends(get_db)):
    return db.query(Period).order_by(Period.start_date.desc()).all()