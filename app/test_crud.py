from sqlalchemy.orm import Session
from app.models import Test
from app.schema import TestCreate

def get_tests(db: Session):
    return db.query(Test).all()

def get_test(db: Session, test_id: int):
    return db.query(Test).filter(Test.id == test_id).first()

def create_test(db:Session, testdb:TestCreate):
    db_test = Test(**testdb.dict())
    print(db_test)
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test

def update_test(db: Session, testdb: Test, updated_item: TestCreate):
    for key, value in updated_item.dict().items():
        setattr(testdb, key, value)
    
    db.commit()
    db.refresh(testdb)
    
    return testdb

def delete_test(db: Session, testdb: Test):
    db.delete(testdb)
    db.commit()
