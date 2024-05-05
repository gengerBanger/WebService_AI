from sqlalchemy import Column, Integer, String
from database.db import Base

class Client(Base):
    __tablename__ = "client"
    __table_args__ = {'schema': 'ws'}

    ID_CLIENT = Column(Integer, primary_key=True, nullable=False)
    AGE = Column(Integer, nullable=False)
    GENDER = Column(String, nullable=False)
    EDUCATION = Column(String, nullable=False)
    MARITAL_STATUS = Column(String, nullable=False)
    CHILD_TOTAL = Column(Integer, nullable=False)
    DEPENDANTS = Column(Integer, nullable=False)
    SOCSTATUS_WORK_FL = Column(Integer, nullable=False)
    SOCSTATUS_PENS_FL = Column(Integer, nullable=False)
    REG_ADDRESS_PROVINCE = Column(String, nullable=False)
    FACT_ADDRESS_PROVINCE = Column(String, nullable=False)
    POSTAL_ADDRESS_PROVINCE = Column(String, nullable=False)
    FL_PRESENCE_FL = Column(Integer, nullable=False)
    OWN_AUTO = Column(Integer, nullable=False)
    PERSONAL_INCOME = Column(Integer, nullable=False)
    Loan_count = Column(Integer, nullable=False)
    CLOSED_FL = Column(Integer, nullable=False)
    TARGET = Column(Integer, nullable=False)