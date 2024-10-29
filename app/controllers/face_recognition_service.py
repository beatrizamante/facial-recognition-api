'''Módulo utilizado para processar a imagem da câmera do usuário
utilizando do facial-recognition'''

import requests
from app.services.camera_feed import CameraFeed
from app.models.face_model import FaceModel

class FaceController:
    '''Classe responsável pelo service de reconhecimento'''
    
    def __init__(self):
        self.model = FaceModel()
        self.view = CameraFeed()
    
    def capture_and_send(self, backend_url):
        frame = self.view.get_frame()
        encoding = self.model.extract_face_encoding(frame)
        
        if encoding: 
            json_data = self.view.format_to_json(encoding)
            response = requests.post(backend_url, data=json_data, 
                                     headers={"Content-Type": "application/json"}, timeout=30)
            return response
        else:
            return {"error": "No face detected"}
        
    