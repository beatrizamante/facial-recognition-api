from app.controllers.face_controller_client import FaceController
from fastapi import FastAPI
import requests
import cv2
from app.models.face_model import FaceModel

app = FastAPI()

class FaceControllerJson:
    '''Classe responsável pelo service de reconhecimento'''
    def __init__(self):
        self.face_model = FaceModel()
    
    async def send_encodes_json_backend(self, frame):
        '''Pega as frames e envia para o backend para comparação.
        Recebe a url do backend como pâemetro e empacota o encoding
        facia em objeto json. Se a resposta do back for 200, autentica com 
        sucesso. Loga depois de 5 tentativas com sucesso. Se não, levanta erro'''

        face_locations = self.face_model.detect_faces(frame)
        user_label = "Identifying..."
        successful_attempts = 0
        total_attempts = 80

        if face_locations:
            encoding = self.face_model.extract_face_encoding(frame, face_locations)
        else:
            encoding = None  
        if encoding is not None:
            _, buffer = cv2.imencode('.jpg', frame)
            json_data = {"image": buffer.tobytes()}  
            response = requests.post(f"{backend_url}/encode/", files={"image": json_data})   
            if response.status_code == 200:
                response_data = response.json()
                user_label = response_data.get("encoding", "name")
                successful_attempts += 1
                if successful_attempts >= 5:
                    return {"message": f"User authenticated successfully as {user_label}"}
            else:
                print("Authentication failed, trying again...") 
        if total_attempts == 0:
            print("Maximum attempts reached.")
        return {"error": "Authentication failed"}

@app.post("/authenticate/")
async def authenticate(backend_url: str):
    controller = FaceController()
    result = await controller.authenticate_user(backend_url)
    return result



        