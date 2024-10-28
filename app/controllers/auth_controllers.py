from app.model.user_model import UserModel
from app.services.image_processing import FaceRecognitionService
class AuthController:
    def __init__(self):
        self.user_model = UserModel()
        self.image_processing = FaceRecognitionService()
        
    def register_user(self, user_id, frame):
        encoding = self.image_processing.extract_face_encoding(frame)
        if encoding is None: 
            return {"Success": False, "message": "No face detected"}

        self.user_model.add_user_enconding(user_id, encoding)
        return {"success": True, "message": "User registered successfully"}
    
    def authenticate_user(self, frame):
        unknown_encoding = self.image_processing.extract_face_encoding(frame)
        if unknown_encoding is None: 
            return {"authenticated": False, "message": "No face detected"}
        
        for user_id, unknown_encoding in self.user_model.db.items():
            return {"authenticated": True, "user_id": user_id}
        
        return {"authenticated": False, "message": "Face not recognized"}
    
    