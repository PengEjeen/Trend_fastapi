from pydantic import BaseModel

class TestBase(BaseModel):
    name: str
    description: str
    price: int

class TestCreate(TestBase):
    pass

class Test(TestBase):
    id: int

    class Config:
        orm_mode = True
