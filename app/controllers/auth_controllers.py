'''Módulo responsável por autenticar e logar o usuário'''

from fastapi import HTTPException
from pydantic import BaseModel
from app.models.user_model import UserModel
from app.services.face_recognition_service import FaceRecognitionService


class AuthController:
    '''Classe responsável por controlar a autenticação e login do usuário.'''

    def __init__(self, db_session):
        self.user_model = UserModel()
        self.db_session = db_session
        self.image_processing = FaceRecognitionService()

    def authenticate_user(self, frame, user_id):
        '''Função responsável por autenticar o usuário caso esse tenha seu
        encoding facial identificado. Recebe uma frame da câmera e retorna
        sucesso ou falha na autenticação.'''
        new_encoding = self.image_processing.extract_face_encoding(frame)

        if new_encoding is None:
            raise HTTPException(status_code=400, detail="No face detected")

        known_encodings = [record.encoding for record in self.db_session.query(UserModel).all()]

        match_found, encoding_to_save = self.image_processing.calculate_face_distance(
            known_encodings, new_encoding
        )

        if match_found:
            return True
        elif encoding_to_save:
            known_encodings.append(encoding_to_save)
            self.user_model.add_user_enconding(user_id, encoding_to_save)
            return {"status": "authenticated", "message": "New encoding added for accuracy"}
        else:
            raise HTTPException(status_code=401, detail="Authentication failed")
