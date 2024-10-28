'''Entrypoint da api'''

from fastapi import FastAPI
from app.routes import auth_route
app = FastAPI()

MATCH_THRESHOLD = 0.6

app.include_router(auth_route.router, prefix="/auth")