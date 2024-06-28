from fastapi import FastAPI
from backend.data.data_router import router as data_router
from backend.ml_model.model_router import router as model_router

app = FastAPI(title="Bank")

app.include_router(data_router)

app.include_router(model_router)