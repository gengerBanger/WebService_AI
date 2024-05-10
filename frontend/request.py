from typing import List
from pandas import DataFrame, Series
import numpy as np
import pandas as pd
import requests

BACKEND_PATH = "http://127.0.0.1:8000"

def get_info():
    url = f"{BACKEND_PATH}/data/all"
    response = requests.get(url)
    return pd.DataFrame(list(response.json()))

def get_split_data(data: DataFrame):
    url = f"{BACKEND_PATH}/model/splitData"
    data_json = data.to_dict(orient='list')
    response = requests.post(url, json=data_json)
    json = response.json()
    X_train = json['scaled_X_train']
    X_test = json['scaled_X_test']
    y_train = json['y_train']
    y_test = json['y_test']
    columns = json['columns']

    return X_train, X_test, y_train, y_test, columns

def get_fit_model(scaled_X_train, y_train):
    url = f"{BACKEND_PATH}/model/fitModel"
    params = {'scaled_X_train': scaled_X_train,
              'y_train': y_train}
    requests.post(url, json=params)

def get_test_model(scaled_X_test, limit=.5):
    url = f"{BACKEND_PATH}/model/testModel"
    params = {'scaled_X_test': scaled_X_test,
              'limit': limit}
    response = requests.post(url, json=params)
    return response.json()['new_labels']

def get_weights(columns: List[str]):
    url = f"{BACKEND_PATH}/model/weights"
    params = {'columns': columns}
    response = requests.post(url, json=params)
    return pd.DataFrame(response.json())

def get_predict(features):
    url = f"{BACKEND_PATH}/model/predictProba"
    params = {'features': features}
    response = requests.post(url, json=params)
    return response.json()['proba']