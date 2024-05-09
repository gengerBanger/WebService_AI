from fastapi import APIRouter
from database.db import get_session


router = APIRouter(tags=['Model'],
                   prefix='/model')