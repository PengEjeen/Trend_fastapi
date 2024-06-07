from sqlalchemy import Column, Integer, String, JSON
from app.database import Base

class User(Base):
        __tablename__ = "users"
        
        user_id = Column(String(30), primary_key=True)
        password = Column(String(100))

class Page(Base):
        __tablename__ = "Page"
        user_id = Column(String(30), primary_key=True)
        page_id = Column(String(30), primary_key=True)
        keyword = Column(String(30))
        df_plot = Column(String(100))
        decompose_plot = Column(String(100))
        predict_plot = Column(String(100))
        test_result = Column(JSON)

        
        
