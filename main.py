'''Entrypoint da api'''

from fastapi import FastAPI
from app.views import auth_view
app = FastAPI()

app.include_router(auth_view.router, prefix="/auth")