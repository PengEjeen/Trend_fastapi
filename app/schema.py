from pydantic import BaseModel

class User_Create(BaseModel):
    user_id: str
    password: str

class Page_Create(BaseModel):
    user_id: str
    page_id: str
    keyword: str
    df_plot: str
    decompose_plot: str
    predict_plot: str
    test_result: dict


