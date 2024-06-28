from typing import List

from fastapi import APIRouter, Depends

from backend.data.schemas import GetAllInfo
from database.db import get_session, SessionLocal
from database.models import Client
from sqlalchemy import select


router = APIRouter(tags=['Data'],
                   prefix='/data')

@router.get('/all', response_model=List[GetAllInfo])
def get_data(db: SessionLocal = Depends(get_session)):
    query = select(Client.ID_CLIENT, Client.AGE, Client.GENDER,
                   Client.EDUCATION, Client.MARITAL_STATUS, Client.CHILD_TOTAL,
                   Client.DEPENDANTS, Client.SOCSTATUS_WORK_FL, Client.SOCSTATUS_PENS_FL,
                   Client.REG_ADDRESS_PROVINCE, Client.FACT_ADDRESS_PROVINCE,
                   Client.POSTAL_ADDRESS_PROVINCE, Client.FL_PRESENCE_FL,
                   Client.OWN_AUTO, Client.PERSONAL_INCOME, Client.Loan_count,
                   Client.CLOSED_FL, Client.TARGET)
    result = db.execute(query).all()
    return result