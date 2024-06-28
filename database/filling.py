import pandas as pd
from database.db import SessionLocal
from database.models import Client

df = pd.read_csv('../data_csv/total_df.csv')

def load_data():
    with SessionLocal() as session:
        session.execute(Client.__table__.insert().values(df.to_dict(orient='records')))
        session.commit()

load_data()