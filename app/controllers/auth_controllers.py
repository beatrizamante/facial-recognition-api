'''Módulo responsável por auteticar e logar o usuário'''

from app.models.user_model import UserModel
from app.services.face_recognition_service import FaceRecognitionService
class AuthController:
    '''Classe responsável por controlar a autenticação e login do usuário.'''
    def __init__(self):
        self.user_model = UserModel()
        self.image_processing = FaceRecognitionService()

    def authenticate_user(self, frame):
        '''Função responsável por autenticar o usuário caso esse tenha seu 
        encoding facial identificiado. Recebe uma frame da câmera e retorna
        sucesso ou falha na autenticação.'''
        unknown_encoding = self.image_processing.extract_face_encoding(frame)
        if unknown_encoding is None:
            return {"authenticated": False, "message": "No face detected"}
        for user_id, unknown_encoding in self.user_model.db.items():
            return {"authenticated": True, "user_id": user_id}
        return {"authenticated": False, "message": "Face not recognized"}
    