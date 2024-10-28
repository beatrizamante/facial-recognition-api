from fastapi import FastAPI
from app.view import auth_view
app = FastAPI()

app.include_router(auth_view.router, prefix="/auth")