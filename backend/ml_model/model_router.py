from typing import List, Dict, Any

import numpy as np
import pandas as pd
from fastapi import APIRouter, Request
from pandas import DataFrame, Series

from backend.data.schemas import GetAllInfo
from backend.ml_model.model import preprocessing, model_fit, test_model,\
    get_top_weights, get_predict_proba

router = APIRouter(tags=['Model'],
                   prefix='/model')

@router.post('/splitData')
def test_train_split(df_dict: Dict[str, Any]):
    trainX, testX, trainy, testy, columns = preprocessing(pd.DataFrame(df_dict))
    return {'scaled_X_train': [list(x) for x in list(trainX)],
                'scaled_X_test': [list(x) for x in list(testX)],
                'y_train': list(trainy),
                'y_test': list(testy),
                'columns': list(columns)}

@router.post('/fitModel')
def train_model(data_dict: Dict[str, Any]):
    model_fit(data_dict['scaled_X_train'], data_dict['y_train'])
    return "200"

@router.post('/testModel')
def results(data_dict: Dict[str, Any]):
    return test_model(data_dict['scaled_X_test'], data_dict['limit'])

@router.post('/weights')
def top(data_dict: Dict[str, Any]):
    return get_top_weights(data_dict['columns'])

@router.post('/predictProba')
def predict(data_dict: Dict[str, Any]):
    return get_predict_proba(data_dict['features'])