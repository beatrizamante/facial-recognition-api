from fastapi import APIRouter, UploadFile, File
import numpy as np
import cv2
from app.controllers.auth_controllers import AuthController


router = APIRouter()
auth_controller = AuthController()

@router.post("register/{user_id}")
async def register_user(user_id: str, file: UploadFile = File(...)):
    frame = np.fromstring(await file.read(), np.uint8)
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    result = auth_controller.register_user(user_id, frame)
    return result

@router.post("/login")
async def login_user(file: UploadFile = File(...)):
    frame = np.fromstring(await file.read(), np.uint8)
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    result = auth_controller.authenticate_user(frame)
    return result