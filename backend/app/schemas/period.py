from pydantic import BaseModel
from datetime import date

class PeriodBase(BaseModel):
    name: str
    code: str
    start_date: date
    end_date: date

class PeriodCreate(PeriodBase):
    pass

class PeriodOut(PeriodBase):
    id: int
    class Config:
        orm_mode = True
