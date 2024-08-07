import numpy as np
import pandas as pd
import pickle
from pandas import DataFrame, Series
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.model_selection import train_test_split

scaler = MinMaxScaler()
encoder = OneHotEncoder(sparse_output=False)
with open('backend/ml_model/model.pkl', 'rb') as f:
    svc_model = pickle.load(f)

def preprocessing(data: DataFrame) -> tuple[np.array, Series, list[str]]:
    model_data = data.drop(['ID_CLIENT', 'REG_ADDRESS_PROVINCE', 'FACT_ADDRESS_PROVINCE', 'POSTAL_ADDRESS_PROVINCE',
                          'FL_PRESENCE_FL', 'OWN_AUTO'], axis=1)
    model_data.rename(columns={'CLOSED_FL': 'Closed_loans'}, inplace=True)

    X = model_data.drop('TARGET', axis=1)
    y = model_data['TARGET']

    categorical_columns = X.select_dtypes(include=['object']).columns.tolist()

    encoded_X = encoder.fit_transform(X[categorical_columns])

    one_hot_X = pd.DataFrame(encoded_X, columns=encoder.get_feature_names_out(categorical_columns))
    X.index = np.arange(0, 15223)
    df_encoded = pd.concat([X, one_hot_X], axis=1)

    cooked_X = df_encoded.drop(categorical_columns, axis=1)

    X_train, X_test, y_train, y_test = train_test_split(cooked_X, y, test_size=0.3, random_state=42)

    scaled_X_train = scaler.fit_transform(X_train)
    scaled_X_test = scaler.transform(X_test)

    return scaled_X_test, y_test, cooked_X.columns

def test_model(scaled_X_test, limit):
    preds_proba = svc_model.predict_proba(scaled_X_test)
    proba_response = preds_proba[:, 1]
    new_labels = proba_response > limit

    new_labels = [int(x) for x in new_labels]

    return {'new_labels': list(new_labels)}

def get_top_weights(columns):
    weights = svc_model.coef_
    weights_df = pd.DataFrame({'Признак': list(columns),
                               'Вес': weights[0],
                               'Модуль веса': abs(weights[0])})
    weights_df = weights_df.sort_values(by='Модуль веса', ascending=False)[['Признак', 'Вес']]
    return weights_df.head(7).to_dict(orient='list')

def get_predict_proba(features):
    client_info = pd.DataFrame(columns=['AGE', 'GENDER', 'EDUCATION', 'MARITAL_STATUS', 'CHILD_TOTAL',
       'DEPENDANTS', 'SOCSTATUS_WORK_FL', 'SOCSTATUS_PENS_FL',
       'PERSONAL_INCOME', 'Loan_count', 'Closed_loans'], data=[features])
    categorical_columns = ['EDUCATION', 'MARITAL_STATUS']
    categorical_encoded = encoder.transform(client_info[categorical_columns])
    categorical_df = pd.DataFrame(categorical_encoded, columns=encoder.get_feature_names_out(categorical_columns))
    df_encoded = pd.concat([client_info, categorical_df], axis=1)

    encoded_client = df_encoded.drop(categorical_columns, axis=1)
    scaled_client = scaler.transform(encoded_client)

    predict = svc_model.predict_proba(scaled_client)

    return {'proba': round(predict[0][1] * 100, 2)}

def get_probs(scaled_X_test):
    return {'probs': list(svc_model.predict_proba(scaled_X_test)[:, 1])}



