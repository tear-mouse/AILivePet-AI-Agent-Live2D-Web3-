from fastapi import FastAPI
from api.api import api_router

app = FastAPI(title="LISABUBU" , description="LISABUBU API", version="1.0.0")

app.include_router(api_router, prefix="")