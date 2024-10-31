import json
from app.services.camera_feed import CameraFeed
from app.models.face_model import FaceModel
from app.models.db_connection import DbConnection

class FaceController:
    #This is a test class to check if everything is running smoothly
    '''Classe responsável pelo service de reconhecimento'''
    def __init__(self):
        self.face_model = FaceModel()
        self.camera_feed = CameraFeed()
        # self.db_encodes = DbConnection()
        
        #Tests with local json
        with open("encoded_faces.json", "r") as f:
            self.encoded_faces = json.load(f)
        
    # async def get_encoded_faces(self):
    #     '''Recupera encodes do banco de dados e compara com o usuário em questão''' 
    #     self.encoded_faces = await self.db_encodes.retrieve_encodings()
    
    # async def authenticate_user(self, backend_url):
    def authenticate_user_clientside(self):
        '''Função responsável por capturar frames e enviar encodings faciais
        até que o usuário seja autenticado.'''
        
        user_label = "Identfying..."
        successful_attempts = 0
        total_attempts = 1000
        # await self.get_encoded_faces()  
        
        try:
            for frame, face_locations in self.camera_feed.get_frame():
                total_attempts -= 1
                
                if face_locations:
                    encoding = self.face_model.extract_face_encoding(frame, face_locations)
                else: 
                    encoding = None
                    
                if encoding is not None:
                    #To test mock_db - using distance                    
                    user_label = self.face_model.get_label(encoding, self.encoded_faces)
                    if user_label:
                        print(f"This is the new label: {user_label}") 
                        successful_attempts += 1
                        
                        print(f"Successful attempts {successful_attempts}")
                        
                        if successful_attempts >= 5:
                            return {"message": f"User authenticated successfully as {user_label}"}
                    else:
                        print("Authentication failed, trying again...")
                        
                # Para comparar sem ser assincrono    
                # time.sleep(0.01)
                    
                if total_attempts == 0:
                    print("Maximum attempts reached.")
                    break
                
        except Exception as e:
            print("An error occurred; ", e)
        finally:
            del self.camera_feed
        return {"error": "Authentication failed"}
    
    
        