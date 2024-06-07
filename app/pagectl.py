from sqlalchemy.orm import Session
from app.models import Page
from app.schema import Page_Create
import hashlib 
from Crypto.Random import get_random_bytes
import base64
import app.rnnctl as rnnctl

def get_userPage(db: Session, user_id: str):
    return db.query(Page).filter(Page.user_id == user_id).all()

def create_page(db: Session, user_id: str, keyword: str):
    #page_id 생성
    random_bytes = get_random_bytes(10)  
    # base64url로 인코딩하여 문자열로 변환합니다.
    page_id = base64.urlsafe_b64encode(random_bytes).decode('utf-8')

    #plot path
    dfplt_pth = f"./plot/dfplt/{user_id}-{page_id}-df.png"
    decomposeplt_pth = f"./plot/decomposeplt/{user_id}-{page_id}-decompose.png"
    predictplt_pth = f"./plot/predictplt/{user_id}-{page_id}-predict.png"

    ###
    #page data 불러오기
    #df 불러오기
    df = rnnctl.get_df(keyword)
    #df_plot 저장
    if not rnnctl.save_dfPlot(df, dfplt_pth):
        return False
    
    #decompose plot 저장
    if not rnnctl.save_decomposePlot(df, decomposeplt_pth):
        return False

    #model 학습
    x_train_uni, y_train_uni, x_test_uni, y_test_uni = rnnctl.preprocessing(df)
    model = rnnctl.train_rnn(x_train_uni, y_train_uni)

    #predict plot 저장
    predictions = rnnctl.save_modelPredict(model, x_test_uni, predictplt_pth)

    #평가 계산
    test_result = rnnctl.modelEval(model, x_test_uni, y_test_uni)
    

    #객체 생성
    pagedb = Page_Create(user_id=user_id, 
                         page_id=page_id, 
                         keyword=keyword,
                         df_plot=f"dfplt/{user_id}/{page_id}/",
                         decompose_plot=f"decomposeplt/{user_id}/{page_id}/",
                         predict_plot=f"predictplt/{user_id}/{page_id}/",
                         test_result=test_result)
    #db 저장
    db_page = Page(**pagedb.dict())
    db.add(db_page)
    print(db_page)
    db.commit()
    db.refresh(db_page)

    return True

