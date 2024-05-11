from typing import Dict, Any
import pandas as pd
from fastapi import APIRouter
from backend.ml_model.model import preprocessing, test_model,\
    get_top_weights, get_predict_proba, get_probs

router = APIRouter(tags=['Model'],
                   prefix='/model')

@router.post('/splitData')
def test_train_split(df_dict: Dict[str, Any]):
    testX, testy, columns = preprocessing(pd.DataFrame(df_dict))
    return {'scaled_X_test': [list(x) for x in list(testX)],
            'y_test': list(testy),
            'columns': list(columns)}
@router.post('/ROC')
def roc_curve(data_dict: Dict[str, Any]):
    return get_probs(data_dict['scaled_X_test'])

@router.post('/testModel')
def results(data_dict: Dict[str, Any]):
    return test_model(data_dict['scaled_X_test'], data_dict['limit'])

@router.post('/weights')
def top(data_dict: Dict[str, Any]):
    return get_top_weights(data_dict['columns'])

@router.post('/predictProba')
def predict(data_dict: Dict[str, Any]):
    return get_predict_proba(data_dict['features'])