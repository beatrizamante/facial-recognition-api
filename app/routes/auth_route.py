'''Rotas para criar e comparar as informações com o que 
existe no banco de dados'''

from fastapi import APIRouter, UploadFile, File
import numpy as np
from cv2 import cv2
from app.controllers.auth_controllers import AuthController


router = APIRouter()
auth_controller = AuthController()

@router.post("/login")
async def login_user(file: UploadFile = File(...)):
    '''Função busca o encoding de um usuário já criado e 
    faz a autenticação de mesmo no aplicatico se os dados baterem.
    Recebe uma file_path e retorna resultado da'''
    frame = np.fromstring(await file.read(), np.uint8)
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    result = auth_controller.authenticate_user(frame)
    return result