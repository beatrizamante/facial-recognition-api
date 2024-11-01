import asyncio
from typing import List, Tuple

import cv2
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from app.models.face_model import FaceModel
from app.controllers.face_controller_backend import FaceControllerJson

app = FastAPI()
face_model = FaceModel()
face_controller = FaceControllerJson()
cascade_classifier = cv2.CascadeClassifier()

class Faces(BaseModel):
    '''Este é um modelo pydantic para definir a estrutura
    da stream data que será enviado ao cv2 para fazer as predições.
    Ele requer uma lista de tuples com 4 integers, ou seja, uma matriz'''
    
    faces: List[Tuple[int, int, int ,int]]
    
async def receive(websocket: WebSocket, queue: asyncio.Queue):
    '''Essa é a função assíncrona que receberá conexões websocket
    do applicativo/página web'''
    bytes = await websocket.receive_bytes()
    try:
        queue.put_nowait(bytes)
    except asyncio.QueueFull:
        pass
    
async def detect_and_authorize(websocket: WebSocket, queue: asyncio.Queue):
    '''Essa função pega a informação recebido e manda isso para o 
    classificador, que então percorre a informação para detectar a 
    presença de um rosto humano, and então retorna a localização da 
    face numa stream de câmera contínua, já que a lista de 4 tuples 
    representa os 4 lados do retângulo'''
    
    successful_attempts = 0
    total_attempts = 200

    while total_attempts > 0:
        bytes = await queue.get()
        data = np.frombuffer(bytes, dtype=np.uint8)
        img = cv2.imdecode(data, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = cascade_classifier.detectMultiScale(gray)
        if len(faces) > 0:
            rgb_image = face_model.convert_to_rgb(img)
            face_locations = face_model.detect_faces(rgb_image)
            encoding = face_model.extract_face_encoding(rgb_image, face_locations)
            if encoding is not None:
                is_match, user_label = face_controller.compare_with_db(encoding, face_locations)
                if is_match:
                    successful_attempts += 1
                    if successful_attempts >= 5:
                        await websocket.send_json({"message": f"User authenticated as {user_label}"})
                else:
                    await websocket.send_json({"message": f"Face not recognized. Retrying..."})
            else:
                await websocket.send_json({"message": f"No face encoding found in frame"})
        else:
            await websocket.send_json({"message": f"No face detected."})
        
        total_attempts -= 1
        
    if successful_attempts < 5:
        await websocket.send_json({"error": "Authentication failed after maximum attempts."})
        
@app.websocket("/face-detection")
async def face_detection(websocket: WebSocket):
    '''Esse é o endpoint que estará enviando requests
    do frontend'''
    
    await websocket.accept()
    queue: asyncio.Queue = asyncio.Queue(maxsize=10)
    face_model = FaceModel() 
    detect_task = asyncio.create_task(detect_and_authorize(websocket, queue, face_model, face_controller))
    try:
        while True:
            await receive(websocket,queue)
    except WebSocketDisconnect:
        detect_task.cancel()
        await websocket.close()

@app.on_event("startup")
async def startup():
    '''Essa função inicia o classificador assim que o aplicativo
    é acionado, assim não é necessário esperar o classificador ser 
    carregado após fazer a request.'''
    
    cascade_classifier.load(
        cv2.data.haarcascades  + "haarcascade_frontalface_default.xml"
    )