import pandas as pd
import requests

BACKEND_PATH = "http://127.0.0.1:8000"
def get_info():
    url = f"{BACKEND_PATH}/data/all"
    response = requests.get(url)
    return pd.DataFrame(list(response.json()))