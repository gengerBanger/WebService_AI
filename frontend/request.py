from typing import List
from pandas import DataFrame
import pandas as pd
import requests

BACKEND_PATH = "http://127.0.0.1:8000"

def get_info():
    url = f"{BACKEND_PATH}/data/all"
    response = requests.get(url)
    return pd.DataFrame(list(response.json()))

def get_probs_ROC(scaled_X_test):
    url = f"{BACKEND_PATH}/model/ROC"
    params = {'scaled_X_test': scaled_X_test}
    response = requests.post(url, json=params)
    return response.json()['probs']

def get_split_data(data: DataFrame):
    url = f"{BACKEND_PATH}/model/splitData"
    data_json = data.to_dict(orient='list')
    response = requests.post(url, json=data_json)
    json = response.json()
    X_test = json['scaled_X_test']
    y_test = json['y_test']
    columns = json['columns']

    return X_test, y_test, columns

def get_test_model(scaled_X_test, limit=.5):
    url = f"{BACKEND_PATH}/model/testModel"
    params = {'scaled_X_test': scaled_X_test,
              'limit': limit}
    response = requests.post(url, json=params)
    return response.json()['new_labels']

def get_predict(features):
    url = f"{BACKEND_PATH}/model/predictProba"
    params = {'features': features}
    response = requests.post(url, json=params)
    return response.json()['proba']