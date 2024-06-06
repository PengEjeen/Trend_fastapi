from sqlalchemy import Column, Integer, String
from app.database import Base

class Test(Base):
        __tablename__ = "tests"
            
        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(String(30))
        description = Column(String(30))
        price = Column(Integer)
