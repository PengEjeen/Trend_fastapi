from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app import database, models, schema, userctl, pagectl
import os

app = FastAPI()

# CORS 설정
origins = [
    "http://localhost:3000",  # React 개발 서버 주소
    # 추가로 허용할 도메인들
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

@app.post("/createUser/")
async def createUser(user_db:schema.User_Create, db:Session=Depends(get_db)):
    response = userctl.create_user(db, user_db)
    return {"response": response}

@app.post("/login/")
async def login(user_db: schema.User_Create, db: Session = Depends(get_db)):
    # 입력된 비밀번호를 해싱하여 비밀번호 비교에 사용
    user_db.password = userctl.hash_password(user_db.password)
    
    # db user 가져옴
    user_compare = userctl.get_user(db, user_db.user_id)
    
    # 사용자 정보가 없거나 비밀번호가 일치하지 않으면 로그인 실패
    if not user_compare or user_compare.password != user_db.password:
        response = False
    else:
        response = True
    
    return {"response": response}


#########
#Page DB

@app.get("/dfplt/{user_id}/{page_id}/")
async def get_dfplt(user_id: str, page_id: str):
    file_path = f"./plot/dfplt/{user_id}-{page_id}-df.png"
    # 이미지 파일이 존재하는지 확인
    if not os.path.exists(file_path):
        return {"error": "File not found"}

    return FileResponse(file_path, media_type='image/png')

@app.get("/decomposeplt/{user_id}/{page_id}/")
async def get_decomposeplt(user_id: str, page_id: str):
    file_path = f"./plot/decomposeplt/{user_id}-{page_id}-decompose.png"
    # 이미지 파일이 존재하는지 확인
    if not os.path.exists(file_path):
        return {"error": "File not found"}

    return FileResponse(file_path, media_type='image/png')

@app.get("/predictplt/{user_id}/{page_id}/")
async def get_decomposeplt(user_id: str, page_id: str):
    file_path = f"./plot/predictplt/{user_id}-{page_id}-predict.png"
    # 이미지 파일이 존재하는지 확인
    if not os.path.exists(file_path):
        return {"error": "File not found"}

    return FileResponse(file_path, media_type='image/png')

@app.get("/createPage/{user_id}/")
async def createPage(user_id: str, keyword: str, db: Session = Depends(get_db)) :
    response = pagectl.create_page(db, user_id, keyword)
    
    return {"response": response}

@app.get("/userPage/{user_id}/")
async def createPage(user_id: str, db: Session = Depends(get_db)) :
    response = pagectl.get_userPage(db, user_id)

    return {"response": response}


if __name__ == "__main__":
   #inner_ip = os.popen("hostname -I").read()
    port = str(input("insert port: "))
    run = f"sudo uvicorn main:app --reload --host=localhost --port={port}"
    os.system(run.replace("\n",""))

