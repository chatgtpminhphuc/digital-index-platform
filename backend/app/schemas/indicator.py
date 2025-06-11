from pydantic import BaseModel
from typing import Optional

class IndicatorBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None

class IndicatorCreate(IndicatorBase):
    pass

class IndicatorOut(IndicatorBase):
    id: int

    class Config:
        orm_mode = True
