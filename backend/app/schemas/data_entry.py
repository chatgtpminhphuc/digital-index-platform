from pydantic import BaseModel

class DataEntryBase(BaseModel):
    indicator_id: int
    organization_id: int
    period_id: int
    value: float

class DataEntryCreate(DataEntryBase):
    pass

class DataEntryOut(DataEntryBase):
    id: int
    class Config:
        orm_mode = True
