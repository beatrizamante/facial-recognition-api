import asyncio
import cv2
from fastapi.websockets import WebSocketState
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.models.face_model import FaceModel
from app.controllers.face_controller_backend import FaceControllerJson

app = FastAPI()
face_model = FaceModel()
face_controller = FaceControllerJson()
cascade_classifier = cv2.CascadeClassifier()
user_label = None
    
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
    total_attempts = 100

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
                is_match, label = face_controller.compare_with_db(encoding)
                user_label = label
                print("User label: ", user_label)  
                
                if is_match:    
                    successful_attempts += 1
                    print("Successfull attempt: ", successful_attempts)
                    
                    if successful_attempts >= 5:
                        print("Successfull attempt login.")
                        await websocket.send_json({"authenticated": True, "message": f"User authenticated as {label}"})
                        await websocket.close()
                        break
                else:
                    await websocket.send_json({"authenticated": False, "message": f"Face not recognized. Retrying..."})
            else:
                await websocket.send_json({"authenticated": False, "message": f"No face encoding found in frame"})
        else:
            await websocket.send_json({"authenticated": False, "message": f"No face detected."})
            
        print("Starts drawing box...........................")  
        print("Img: ", img)
        print("Face locations: ", face_locations)
        print("User label: ", user_label)  
        img_box = face_model.draw_boxes(img, face_locations, label if successful_attempts > 0 else None) 
        print("Draws box...........................")
        
        _, buffer = cv2.imencode('.jpg', img_box)
        frame_with_box = buffer.tobytes()
        await websocket.send_bytes(frame_with_box)
        
        total_attempts -= 1
        print("Total attempts: ", total_attempts)
        
    if successful_attempts < 5:
        await websocket.send_json({"error": "Authentication failed after maximum attempts."})
        await websocket.close()
        return
        
@app.websocket("/face-detection")
async def face_detection(websocket: WebSocket):
    '''Esse é o endpoint que estará enviando requests
    do frontend'''
    
    await websocket.accept()
    queue: asyncio.Queue = asyncio.Queue(maxsize=10)
    detect_task = asyncio.create_task(detect_and_authorize(websocket, queue))
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