import asyncio
from typing import List
import cv2
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.models.face_model import FaceModel
from app.controllers.auth_controller import FaceControllerJson
from pydantic import BaseModel

app = FastAPI()
face_model = FaceModel()
face_controller = FaceControllerJson()
cascade_classifier = cv2.CascadeClassifier()
user_label = "Desconhecido"

# class Face(BaseModel):
#     '''Modelo base - tipagem do que é esperado para desenhar os quadrados no front.'''
#     x: int
#     y: int
#     width: int
#     height: int
#     label: str = "Desconhecido"  

# class FacesList(BaseModel):
#     '''Os modelos de desenho são enviados como objetos JSON em lista, então é necessário
#     torná-los em uma lista aqui.'''
#     facesList: List[Face] 


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
    presença de um rosto humano, retornando a localização da 
    face numa stream de câmera contínua, já que a lista de 4 tuples 
    representa os 4 lados do retângulo e autorizando caso o usuário
    exista na base de dados.'''
    
    successful_attempts = 0
    total_attempts = 20

    while total_attempts > 0:
        bytes = await queue.get()
        data = np.frombuffer(bytes, dtype=np.uint8)
        img = cv2.imdecode(data, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
         
        faces = cascade_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        # faces_output = []
        if len(faces) == 1:
            
            rgb_image = face_model.convert_to_rgb(img)
            face_locations = face_model.detect_faces(rgb_image)
            print("Face locations: ", face_locations)
            
            if not face_locations:
                print("Face found by Haar cascade, but no face locations detected.")
                total_attempts -= 1
                continue
          
            encoding = face_model.extract_face_encoding(rgb_image, face_locations)
            if encoding is not None:
                label, is_match = await face_controller.compare_with_db(encoding)
                user_label = label
                
                #Essa parte seria para desenhar os retângulos no front, caso um dia precise
                # for (x, y, w, h) in faces: 
                #     face_instance = Face(x=x, y=y, width=w, height=h, label=user_label)
                #     faces_output.append(face_instance)
                # faces_list = FacesList(facesList=faces_output)
                #Finaliza
                
                if is_match:
                    successful_attempts += 1
                    print("Successfull attempt: ", successful_attempts)
                    
                    if successful_attempts >= 5:
                        print("Successfull attempt login.")
                        await websocket.send_json({"authenticated": True, "message": f"Usuário autenticado como {label}"})
                        await websocket.close()
                        break
                else:
                    print("No face on database")
                    await websocket.send_json({"authenticated": False, "message": f"Rosto não reconhecido no banco, tentando novamente..."})
            else:
                print("No face encoding")
                await websocket.send_json({"authenticated": False, "message": f"Nenhum encoding encontrado na imagem."})
        else:
            print("No face detected or multiples faces detected")
            # faces_list = FacesList(facesList=[])
            await websocket.send_json({"authenticated": False, "message": f"Nenhum rosto detectado, ou multiplos rostos detectados, favor, apenas um rosto para login."})
            
        # await websocket.send_json(faces_list.model_dump())
        
        total_attempts -= 1
        print("Total attempts:        ", total_attempts)        
    if successful_attempts < 5:
        await websocket.send_json({"error": "Authentication failed after maximum attempts."})
        await websocket.close()
        return
        
@app.websocket("/face-detection")
async def face_detection(websocket: WebSocket):
    '''Esse é o endpoint que estará enviando requests do frontend para stream de video.'''
    await websocket.accept()
    queue: asyncio.Queue = asyncio.Queue(maxsize=1)
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