import time
import requests
import json
from app.services.camera_feed import CameraFeed
from app.models.face_model import FaceModel

class FaceController:
    '''Classe responsável pelo service de reconhecimento'''
    def __init__(self):
        self.face_model = FaceModel()
        self.camera_feed = CameraFeed()
        
        with open("encoded_faces.json", "r") as f:
            self.encoded_faces = json.load(f)
    
    def authenticate_user(self, backend_url):
        '''Função responsável por capturar frames e enviar encodings faciais
        até que o usuário seja autenticado.'''
        
        successful_attempts = 0
        total_success = 5
        max_attempts = 0
        total_attempts = 10
        try:
            while successful_attempts < total_success and max_attempts < total_attempts:
                max_attempts += 1
                frame, face_locations = self.camera_feed.get_frame() 
                encoding = self.face_model.extract_face_encoding(frame, face_locations)

                # print("Face encoding:", encoding)

                if encoding is not None:
                    #To test mock_db
                    for known in self.encoded_faces:
                        known_encoded = known['encoding']
                        
                        print("Face encoding:", known_encoded)
                        
                        distance = self.face_model.calculate_face_distance(known_encoded, encoding)
                        
                        print("Distance: ", distance)
                        
                        if distance < 0.5:
                            print(f"Authenticated as {known['label']}")
                            successful_attempts += 1
                            return {"message": f"User authenticated successfully as {known['label']}"}
                                              
                      
                    # json_data = self.camera_feed.format_to_json(encoding)
                    # print("Json object:", json_data)
                    # response = requests.post(backend_url, data=json_data,
                    #                          headers={"Content-Type": "application/json"}, timeout=30)

                    # if response.status_code == 200:  
                    #     successful_attempts += 1
                        
                    #     if successful_attempts >= total_success:
                    #         print("User authenticated successfully!")
                    #         return response.json()
                    # else:
                    #     print("Authentication failed. Trying again...")
                else:
                    print("No face detected, trying again...")
                    return {"error": "Authentication failed"}

                time.sleep(2)
                
        except Exception as e:
            print("An error occured; ", e)
        finally:
            del self.camera_feed
        return {"error": "Authentication failed"}
