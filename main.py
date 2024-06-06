from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from app import test_crud, database, models, schema
import os

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    database.create_tables()

@app.get("/")
async def getDEV():
    message = "hello"
    return{"message": message} 

@app.get("/tests")
async def get_tests(db: Session = Depends(get_db)):
    try:
        tests = test_crud.get_tests(db)
        return tests
    
    except:
        return HTTPException(status_code=404, detail="db not found")

@app.get("/tests/{test_id}")
async def get_tests(test_id: int, db: Session = Depends(get_db)):
    try:
        tests = test_crud.get_test(db, test_id)
        return tests
    
    except:
        return HTTPException(status_code=404, detail="db not found")


@app.post("/tests/")
async def create_test(test_db:schema.TestCreate, db:Session=Depends(get_db)):
    db_test = test_crud.create_test(db, test_db)
    return db_test

@app.put("/tests/{test_id}")
async def update_test(test_id:int, updated_test: schema.TestCreate, db:Session=Depends(get_db)):
    db_test = test_crud.get_test(db, test_id)
    if db_test is None:
        raise HTTPException(status_code=404, detail="Item not found")
    result = test_crud.update_test(db, db_test, updated_test)
    return result


if __name__ == "__main__":
   #inner_ip = os.popen("hostname -I").read()
    port = str(input("insert port: "))
    run = f"sudo uvicorn main:app --reload --host=localhost --port={port}"
    os.system(run.replace("\n",""))

