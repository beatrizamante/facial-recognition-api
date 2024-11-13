import asyncio
from typing import List
import cv2
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.models.face_model import FaceModel
from app.models.camera_model import CameraModel
from app.controllers.db_controller import FaceControllerJson
from app.services.auth_services import decode_token
from pydantic import BaseModel

app = FastAPI()
face_model = FaceModel()
camera_model = CameraModel()
face_controller = FaceControllerJson()
cascade_classifier = cv2.CascadeClassifier()

connections = {}

#Parte para desenhar os retângulos no front
class Face(BaseModel):
    '''Modelo base - tipagem do que é esperado para desenhar os quadrados no front.'''
    x: int
    y: int
    width: int
    height: int
    label: str = "Desconhecido"  

class FacesList(BaseModel):
    '''Os modelos de desenho são enviados como objetos JSON em lista, então é necessário
    torná-los em uma lista aqui.'''
    facesList: List[Face] 
#______

async def receive(websocket: WebSocket, queue: asyncio.Queue):
    '''Essa é a função assíncrona que receberá conexões websocket
    do applicativo/página web, colocando os base64 das imagens em uma file'''
    bytes = await websocket.receive_bytes()
    try:
        queue.put_nowait(bytes)
    except asyncio.QueueFull:
        pass
    
#TODO 
#Separar funções com princípio de responsábilidade única    
#Da de simplificar muito a detect_and_authorize, mas vou deuxar assim no momento para entregar 8D
    
async def detect_and_authorize(websocket: WebSocket, queue: asyncio.Queue):
    '''Essa função pega a informação recebido e manda isso para o 
    classificador, que então percorre a informação para detectar a 
    presença de um rosto humano, retornando a localização da 
    face numa stream de câmera contínua, já que a lista de 4 tuples 
    representa os 4 lados do retângulo e autorizando caso o usuário
    exista na base de dados.'''
    
    successful_attempts = 0
    total_attempts = 100

    while total_attempts > 0:
        faces_output = []
        bytes = await queue.get()
        data = np.frombuffer(bytes, dtype=np.uint8)
        img = cv2.imdecode(data, 1)
        
        if camera_model.camera_width == 0 or camera_model.camera_height == 0:
            height, width = img.shape[:2]
            camera_model.update_dimensions(width, height)
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        faces = cascade_classifier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=6, minSize=(30, 30))
        
        if len(faces) > 1:
            print("Multiples faces detected")
            await websocket.send_json({"authenticated": False, "message": f"Multiplos rostos detectados, favor deixar apenas um usuário na tela"})
            continue
        
        if len(faces) > 0:   
            rgb_image = face_model.convert_to_rgb(img)
            face_locations = face_model.detect_faces(rgb_image)
            print("Face locations: ", face_locations)
            
            if not face_locations:
                print("Face found by Haar cascade, but no face locations detected.")
                total_attempts -= 1
                continue
            
            camera_model.find_center_face(face_locations)
            if not camera_model.check_if_centered():
                total_attempts -= 1   
                print("Face not centered")
                await websocket.send_json({"authenticated": False, "message": "Rosto não está centralizado"})
                continue
          
            encoding = face_model.extract_face_encoding(rgb_image, face_locations)
            
            if encoding is not None:
                label, mail, is_match = await face_controller.compare_with_db(encoding)
                print(f"Label________________{label}")
                print(f"Mail__________________{mail}")
                print(f"Is_Match__________________{is_match}")
                
                #Aqui envia as coordenadas do rosto na tela e o label da pessa se essa já tiver um, senão envia como desconhecido
                #Essa função não seria necessária, mas o front está pegando o label dela, então vou deixar ela aqui
                for (x, y, w, h) in faces: 
                    face_instance = Face(x=x, y=y, width=w, height=h, label=label)
                    faces_output.append(face_instance)
                faces_list = FacesList(facesList=faces_output)
                #End
                
                if is_match:
                    # if websocket.user_info and websocket.user_info.get('user_id') == label:
                    successful_attempts += 1
                    
                    if successful_attempts >= 5:

                        print("Successfull attempt login.")
                        await websocket.send_json({"authenticate": True, "label": label, "mail": mail, "message": f"Usuário autenticado como {label}"})
                        break
                else:
                    await websocket.send_json({"authenticate": False, "message": f"Rosto não reconhecido no banco, tentando novamente..."})
            else:
                await websocket.send_json({"authenticate": False, "message": f"Nenhum encoding encontrado na imagem."})
        else:
            faces_list = FacesList(facesList=[])
            await websocket.send_json({"authenticated": False, "message": f"Nenhum rosto detectado."})
            
        await websocket.send_json(faces_list.model_dump())
        
        total_attempts -= 1
    if successful_attempts < 5:
        print("Atintigu maximo de attemps")
        await websocket.send_json({"error": "Authentication failed after maximum attempts."})
        return
      
@app.websocket("/face-detection")
async def face_detection(websocket: WebSocket):
    '''Esse é o endpoint que estará enviando requests do frontend para stream de video.
    Também separa cada conexão de websocket em diferentes dispositivos em diferentes filas.'''

    await websocket.accept()
    
    #______________________________________
    # token = websocket.headers.get("sec-websocket-protocol")
    # auth_token = token.split(",")[0]
    # user_info = decode_token(auth_token)
    
    # group_token = token.split(",")[1]
    # fetch_group_members = fetch_group_members(token, group_token)
    
    # print("User_info__________________", user_info)    
    # print("Group Members__________________", fetch_group_members)    
    #_______________________________________
    
    queue: asyncio.Queue = asyncio.Queue(maxsize=1)
    
    connections[websocket] = queue
    detect_task = asyncio.create_task(detect_and_authorize(websocket, queue))
    try:
        while True:
            await receive(websocket,queue)
    except WebSocketDisconnect:
        detect_task.cancel()
        del connections[websocket]
        await websocket.close()

@app.on_event("startup")
async def startup():
    '''Essa função inicia o classificador assim que o aplicativo
    é acionado, assim não é necessário esperar o classificador ser 
    carregado após fazer a request.'''
    
    await face_controller.initialize()
    
    cascade_classifier.load(
        cv2.data.haarcascades  + "haarcascade_frontalface_default.xml"
    )