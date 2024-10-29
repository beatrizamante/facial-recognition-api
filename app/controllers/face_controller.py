import requests
from app.services.camera_feed import CameraFeed
from app.models.face_model import FaceModel

class FaceController:
    '''Classe responsável pelo service de reconhecimento'''
    def __init__(self):
        self.model = FaceModel()
        self.view = CameraFeed()
    
    def authenticate_user(self, backend_url):
        '''Função responsável por capturar frames e enviar encodings faciais
        até que o usuário seja autenticado.'''
        while True:
            frame = self.view.get_frame() 
            encoding = self.model.extract_face_encoding(frame)
            
            if encoding is not None:  
                print("User authenticated successfully! - Se encontrar um rosto, irá retornar sucesso")
                json_data = self.view.format_to_json(encoding)
                print("Face encoding:", encoding)
                print("JSON Data:", json_data) 
                
                # response = requests.post(backend_url, data=json_data,
                #                          headers={"Content-Type": "application/json"}, timeout=30)
                
                # if response.status_code == 200:  
                #     print("User authenticated successfully!")
                #     # return response.json()
                #     break 
                # else:
                #     print("Authentication failed. Trying again...")
            else:
                print("No face detected, trying again...")
                return {"error": "Authentication failed"}

    def __del__(self):
        '''Função responsável por parar a captura da câmera'''
        del self.view  
