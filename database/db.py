from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine
from config import *

URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

meta = MetaData()

Base = declarative_base(metadata=meta)

engine = create_async_engine(URL)

SessionLocal = sessionmaker(bind=engine,
                       autoflush=False,
                       autocommit=False)