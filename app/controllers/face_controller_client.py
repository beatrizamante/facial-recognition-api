import json
import threading
import time
from app.services.camera_feed import CameraFeed
from app.models.face_model import FaceModel

class FaceController:
    #This is a test class to check if everything is running smoothly
    '''Classe responsável pelo service de reconhecimento'''
    def __init__(self):
        self.face_model = FaceModel()
        self.camera_feed = CameraFeed()
        self.user_label = None
        
        #Tests with local json
        with open("encoded_faces.json", "r") as f:
            self.encoded_faces = json.load(f)
            
        # self.capture_thread = threading.Thread(target=self.camera_feed.capture_frame)
        # self.capture_thread.start()
        
    # async def get_encoded_faces(self):
    #     '''Recupera encodes do banco de dados e compara com o usuário em questão''' 
    #     self.encoded_faces = await self.db_encodes.retrieve_encodings()
    
    # async def authenticate_user(self, backend_url):
    
    def authenticate_user_clientside(self):
        '''Função responsável por capturar frames e enviar encodings faciais
        até que o usuário seja autenticado.'''
        
        user_label = "Identfying..."
        successful_attempts = 0
        total_attempts = 300
        # await self.get_encoded_faces()  
        
        try:
            # while successful_attempts < 5 and total_attempts != 0:
            #     frame, face_locations = self.camera_feed.get_frame()
            for frame, face_locations in self.camera_feed.get_frame():
                total_attempts -= 1 
                if not self.user_label and face_locations:
                    encoding = self.face_model.extract_face_encoding(frame, face_locations)   
                    if encoding is not None:
                        label = self.face_model.get_label(encoding, self.encoded_faces)
                        if label:
                            successful_attempts += 1                        
                            if successful_attempts >= 5:
                                self.user_label = label
                                print(f"Authenticated with {self.user_label}")
                                return {"message": f"User authenticated successfully as {user_label}"}
                    else:   
                        print("Authentication failed, trying again...")
                        
                # Para comparar sem ser assincrono    
                time.sleep(0.01)
                    
                if total_attempts == 0:
                    print("Maximum attempts reached, .")
                    return {"error": "Authentication failed"}
                
        except Exception as e:
            print("An error occurred; ", e)
        finally:
            del self.camera_feed
            # self.camera_feed.stop_camera()
            # self.capture_thread.join()
    
    
        