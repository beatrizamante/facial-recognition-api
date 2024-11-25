import asyncio
from typing import List
import cv2
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.models.face_model import FaceModel
from app.models.camera_model import CameraModel
from app.controllers.face_controller_backend import FaceControllerJson
from app.services.auth_service import fetch_group_members, parse_token
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
#__________________________________________

async def receive(websocket: WebSocket, queue: asyncio.Queue):
    '''Essa é a função assíncrona que receberá conexões websocket
    do applicativo/página web, colocando os base64 das imagens em uma file'''
    bytes = await websocket.receive_bytes()
    try:
        queue.put_nowait(bytes)
    except asyncio.QueueFull:
        pass

async def detect_faces_in_image(img: np.ndarray) -> List:
    '''Função detecta faces numa imagem.
    Parâmetro: 
        img: imagem em um numpy array.
    Retorna:
        Coordenadas de localização da imagem
    '''
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cascade_classifier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=6, minSize=(30, 30))

async def process_face(img: np.ndarray, faces: List, websocket: WebSocket) -> bool:
    '''Processa as faces presentes na imagem e compara essas com o banco de dados.
    Parâmetros: 
        img: imagem em np.array,
        faces: lista de coordenadas e label do rosto encontrado na imagem
        websocket: conexão websocket ativa
    Retorna:
        is_match: boolean caso o rosto dê match com algum encotrado na base de dados
        mail: email do usuário encontrado no banco de dados,
        label: nome do usuário encontrado no banco de dados. 
        '''
        
    faces_for_display = []
    rgb_image = face_model.convert_to_rgb(img)
    face_locations = face_model.detect_faces(rgb_image)

    if not face_locations:
        await websocket.send_json({"message": "Nenhuma face detectada"})
        return None, None, False

    camera_model.find_center_face(face_locations)
    if not camera_model.check_if_centered():
        await websocket.send_json({"message": "Face não centralizada"})
        return None, None, False

    encoding = face_model.extract_face_encoding(rgb_image, face_locations)
    if encoding is None:
        await websocket.send_json({"message": "Encoding não encontrado"})
        return None, None, False
    
    label, mail, is_match = await face_controller.compare_with_db(encoding)
    
    #Essa parte seria para enviar as coordenadas para o front como objeto json e de lá desenha retângulos ao redor do rosto da pessoa
    #Dá de tirar, mas o flutter está pegando o label (nome do usuário) daqui
    #Nesse refatoramento, por conta de ter uns milissegundos entre as frames, os retângulos ficam piscando, mas como nem estamos usando,
    #ninguém liga - mas fica a dica, no codigo não refatorado ele funciona em real-time mesmo
    for (x, y, w, h) in faces:
        faces_for_display.append(Face(x=x, y=y, width=w, height=h, label=label))

    await websocket.send_json(FacesList(facesList=faces_for_display).model_dump())
    #_______________________________________
    
    return label, mail, is_match

async def authenticate_user(websocket: WebSocket, label: str, db_mail: str):
    '''Função responsável por autenticar o usuário pela Microsoft.
    Parâmetros:
      websocket: Conexão websocket ativa,
      label: label do usuário que está sendo autenticado,
      mail: email do usuário que está sendo autenticado
    Retona:
      Boolen true caso a função tenha encontrado o usuário no grupo de emails correto, 
      Boolean false caso não tenha encontrado o usuário. 
    '''
    try:
        token_header = websocket.headers.get("sec-websocket-protocol")
        tokens = parse_token(token_header)
        group_members = await fetch_group_members(tokens["auth_token"], tokens["group_token"])
        print(f"Is it trying to get the token? {group_members} and {tokens}")

        if db_mail.lower() in (member.lower() for member in group_members):
            await websocket.send_json({"authenticate": True, "message": f"Usuário {label} autenticado"})
            return True
        
    except Exception as e:
        await websocket.send_json({"authenticate": False, "message": f"Erro na autenticação: {str(e)}"})
    
    await websocket.send_json({"authenticate": False, "message": f"Usuário {label} não encontrado na tabela da Microsoft."})
    return False

async def detect_and_authorize(websocket: WebSocket, queue: asyncio.Queue):
    """Função assíncrona que faz a junção de todas as funções."""
    successful_attempts = 0
    total_attempts = 100
    
    while total_attempts > 0:
        bytes_data = await queue.get()
        data = np.frombuffer(bytes_data, dtype=np.uint8)
        img = cv2.imdecode(data, 1)
        
        if camera_model.camera_width == 0 or camera_model.camera_height == 0:
            height, width = img.shape[:2]
            camera_model.update_dimensions(width, height)
    
        faces = await detect_faces_in_image(img)
        
        if len(faces) > 1:
            await websocket.send_json({"message":  "Múltiplos rostos detectados"})
            continue
        
        if len(faces) > 0:
            is_match, label, mail = await process_face(img, faces, websocket)
            if is_match:
                successful_attempts += 1
                if successful_attempts >= 5:
                    if await authenticate_user(websocket, label, mail):
                        break
            else:
                await websocket.send_json({"message":  "Rosto não reconhecido no banco"})
        else:
            await websocket.send_json({"message":  "Nenhum rosto detectado"})
        total_attempts -= 1
        
    await websocket.send_json({"message":  "Máximo de tentativas atingido"})    
      
@app.websocket("/face-detection")
async def face_detection(websocket: WebSocket):
    '''Esse é o endpoint que estará enviando requests do frontend para stream de video.
    Separa cada conexão de websocket em diferentes dispositivos em diferentes filas para evitar reconhecimento aleatórios.'''

    await websocket.accept()

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
    carregado após fazer a request. Também carrega os usuários do n
    banco ao iniciar o websocket para serem chamados apenas uma vez.'''
    
    await face_controller.initialize()
    
    cascade_classifier.load(
        cv2.data.haarcascades  + "haarcascade_frontalface_default.xml"
    )
    
    
    
    #_______________________________________________________

#Esse aqui funciona, caso precise    
# async def detect_and_authorize(websocket: WebSocket, queue: asyncio.Queue):
#     '''Essa função pega a informação recebido e manda isso para o 
#     classificador, que então percorre a informação para detectar a 
#     presença de um rosto humano, retornando a localização da 
#     face numa stream de câmera contínua, já que a lista de 4 tuples 
#     representa os 4 lados do retângulo e autorizando caso o usuário0
#     exista na base de dados.'''
    
#     successful_attempts = 0
#     total_attempts = 100

#     while total_attempts > 0:
#         faces_output = []
#         bytes = await queue.get()
#         data = np.frombuffer(bytes, dtype=np.uint8)
#         img = cv2.imdecode(data, 1)
        
#         if camera_model.camera_width == 0 or camera_model.camera_height == 0:
#             height, width = img.shape[:2]
#             camera_model.update_dimensions(width, height)
        
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
#         faces = cascade_classifier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=6, minSize=(30, 30))
        
        
#         print(f"Finding faces_______________________{len(faces)}")
#         if len(faces) > 1:
#             print("Multiples faces detected")
#             await websocket.send_json({"authenticate": False, "message": f"Multiplos rostos detectados, favor deixar apenas um usuário na tela"})
#             continue
        
#         if len(faces) > 0:   
#             rgb_image = face_model.convert_to_rgb(img)
#             face_locations = face_model.detect_faces(rgb_image)
#             print("Face locations: ", face_locations)
            
#             if not face_locations:
#                 print("Face found by Haar cascade, but no face locations detected.")
#                 total_attempts -= 1
#                 continue
            
#             camera_model.find_center_face(face_locations)
#             if not camera_model.check_if_centered():
#                 total_attempts -= 1   
#                 print("Face not centered")
#                 await websocket.send_json({"authenticate": False, "message": "Rosto não está centralizado"})
#                 continue
          
#             encoding = face_model.extract_face_encoding(rgb_image, face_locations)
        
#             if encoding is not None:
#                 label, mail, is_match = await face_controller.compare_with_db(encoding)
                
#                 #Aqui envia as coordenadas do rosto na tela e o label da pessa se essa já tiver um, senão envia como desconhecido
#                 #Essa função não seria necessária, mas o front está pegando o label dela, então vou deixar ela aqui
#                 for (x, y, w, h) in faces: 
#                     face_instance = Face(x=x, y=y, width=w, height=h, label=label)
#                     faces_output.append(face_instance)
#                 faces_list = FacesList(facesList=faces_output)
#                 #End
                
#                 if is_match:
#                     successful_attempts += 1
                    
#                     if successful_attempts >= 5:
                        
#                         #_____________________________Checking microsoft authentication
#                         try: 
#                             token_header = websocket.headers.get("sec-websocket-protocol")
#                             tokens = parse_token(token_header)

#                             user_info = decode_token(tokens["auth_token"])
#                             group_members = await fetch_group_members(tokens["auth_token"], tokens["group_token"])
#                             user_mail = user_info.get("mail")
#                             is_in_group = await is_member_in_group(group_members, user_mail)
                            
#                             if is_in_group:
#                                 print(f"Successfull attempt login. {user_mail} found in group")
#                                 await websocket.send_json({
#                                     "authenticate": True,
#                                     "label": label,
#                                     "mail": mail,
#                                     "message": f"Usuário autenticado como {label}."
#                                 })
#                                 break
                            
#                         except Exception as e:
#                             await websocket.send_json({
#                                 "authenticate": False,
#                                 "message": f"Erro durante a autenticação do grupo: {str(e)}"
#                             })
                        
#                         #_____________________________

#                 else:
#                     await websocket.send_json({"authenticate": False, "message": f"Rosto não reconhecido no banco, tentando novamente..."})
#             else:
#                 await websocket.send_json({"authenticate": False, "message": f"Nenhum encoding encontrado na imagem."})
#         else:
#             faces_list = FacesList(facesList=[])
#             await websocket.send_json({"authenticate": False, "message": f"Nenhum rosto detectado."})
            
#         await websocket.send_json(faces_list.model_dump())
        
#     total_attempts -= 1
#     print("Atintigu maximo de attemps")
#     await websocket.send_json({"error": "Reconhecimento atingiu o máximo de tentativas."})
#     return