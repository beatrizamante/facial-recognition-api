from fastapi import FastApi
from app.api.routes import router

app = FastAPI()

app.include_router(router)