import requests
import pandas as pd
from ast import literal_eval
import matplotlib.pyplot as plt
from datetime import datetime
from statsmodels.tsa.seasonal import seasonal_decompose
import numpy as np
from sklearn.model_selection import train_test_split

SEQLEN = 10

#get raw data from naver api
def get_df(keyword):
    url = "https://openapi.naver.com/v1/datalab/search"
    now = datetime.now()
    # 원하는 형식으로 문자열로 변환 (예: "YYYY-MM-DD")
    current_date_str = now.strftime("%Y-%m-%d")


    client_id = "pt4OvN2fzzLJgFJxIaQf"
    client_secret = "deXXmDzy6w"

    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
        "Content-Type": "application/json"
    }

    body = {
        "startDate": "2016-01-01",
        "endDate": current_date_str,
        "timeUnit": "date",
        "keywordGroups": [
            {
                "groupName": keyword,
                "keywords": [keyword]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        raw_data = response.json()

        #set Time
        #dict_data = literal_eval(raw_data)
        data = raw_data['results'][0]['data']
        df = pd.DataFrame.from_dict(data)
        df["period"] = pd.date_range(start=df["period"][0], periods=len(df), freq='D')
        df.set_index('period', inplace=True) # Set the date column as index

        print("get df...")
        return df
    else:
        print("Error Code:", response.status_code)
        return False
    

#save df ratio plot
def save_dfPlot(df, path):
    try:
        print("save df plot")
        plt.plot(df["ratio"])
        plt.savefig(path)
        plt.close()

        return True   
    except Exception as e:
        print("error: ", e)
        return False 

def save_decomposePlot(df, path):
    try:
        print("save df decompose plot")
        result = seasonal_decompose(df, model='additive')
        plt.rcParams['figure.figsize'] = [12, 8]
        result.plot()
        plt.savefig(path)
        plt.close()

        return True
    except:
        return False

def univariate_data(dataset, start_index, end_index, data_window, target):
  data, labels = [], []

  start_index = start_index + data_window
  if end_index is None:
    end_index = len(dataset) - target

  for i in range(start_index, end_index):
    indices = range(i-data_window, i)
    # Ensure the sliced data is 1-dimensional
    data.append(np.reshape(dataset[indices].values, (data_window, 1))) # Extract underlying NumPy array 
    labels.append(dataset[i+target])
  return np.array(data), np.array(labels)


################################################################################################
###use simple rnn
def preprocessing(df):
    print("preprocessing . . .")
    try:
        #split 0.2 0.8
        train_df, test_df = train_test_split(df, test_size=0.2, shuffle=False)

        #preprocess df window 10
        x_train_uni, y_train_uni = univariate_data(train_df["ratio"], 0, len(train_df), SEQLEN, 0)
        x_test_uni, y_test_uni = univariate_data(test_df["ratio"], 0, len(test_df), SEQLEN, 0)
        return x_train_uni, y_train_uni, x_test_uni, y_test_uni

    except Exception as e:
        print("error: ", e)
        return False
    
def train_rnn(x_train_uni, y_train_uni):
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import SimpleRNN, Dense
    # RNN 모델 생성

    print("Training . . .")
    model = Sequential()
    model.add(SimpleRNN(50, activation='tanh', input_shape=(SEQLEN, 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')

    # 모델 학습
    model.fit(x_train_uni, y_train_uni, epochs=100, batch_size=10, validation_split=0.2)

    return model

def save_modelPredict(model, x_test_uni, path):
    print("Predicting . . .")
    # 마지막 10일치 데이터를 입력으로 사용하여 예측 시작
    input_data = x_test_uni[-1]

    # 30일치 예측
    predicted_data = []
    for i in range(30):
        # 모델을 사용하여 다음 시점 데이터 예측
        next_prediction = model.predict(np.expand_dims(input_data, axis=0))[0][0] #1 차원 추가 후 요소 선택
        
        # 예측값을 기록
        predicted_data.append(next_prediction)
        
        # 다음 시점을 위해 입력 데이터 업데이트
        input_data = np.roll(input_data, -1) #왼쪽 시프트 연산
        input_data[-1] = next_prediction

    plt.plot(predicted_data, label='predict')
    plt.savefig(path)
    
    return predicted_data


def modelEval(model, x_uni, y_uni):
    predictions = model.predict(x_uni)
    # ME 계산
    me = np.mean(predictions - y_uni)
    # RMSE 계산
    rmse = np.sqrt(np.mean((predictions - y_uni) ** 2))
    # MAE 계산
    mae = np.mean(np.abs(predictions - y_uni))
    # MPE 계산
    mpe = np.mean((predictions - y_uni) / y_uni) * 100
    # MAPE 계산
    mape = np.mean(np.abs((predictions - y_uni) / y_uni)) * 100
    # MASE 계산
    mase = np.mean(np.abs(predictions - y_uni)) / np.mean(np.abs(y_uni[1:] - y_uni[:-1]))
    # Theil's U 계산
    theils_u = (np.sqrt(np.mean((predictions - y_uni) ** 2)) /
                (np.sqrt(np.mean(predictions ** 2)) + np.sqrt(np.mean(y_uni ** 2))))
    
    return {"me": me, "rmse": rmse, "mae": mae, "mpe": mpe, "mape": mape, "mase": mase, "theils_u": theils_u}
