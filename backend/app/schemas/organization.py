from pydantic import BaseModel

class OrganizationBase(BaseModel):
    name: str
    code: str

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationOut(OrganizationBase):
    id: int
    class Config:
        orm_mode = True
