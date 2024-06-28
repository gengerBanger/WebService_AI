from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import MetaData, create_engine
from config import *

URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

meta = MetaData()

Base = declarative_base(metadata=meta)

engine = create_engine(URL)

SessionLocal = sessionmaker(bind=engine,
                       autoflush=False,
                       autocommit=False)

def get_session():
    with SessionLocal() as session:
        return session