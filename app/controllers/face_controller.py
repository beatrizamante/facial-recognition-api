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
        total_attempts = 45
        try:
            for frame, face_locations in self.camera_feed.get_frame("Authenticating..."):
                print(f"Maximum attempts: {total_attempts}")
                total_attempts -= 1
                
                if face_locations:
                    encoding = self.face_model.extract_face_encoding(frame, face_locations)
                else: 
                    encoding = None
                    
                if encoding is not None:
                    #To test mock_db - usng distance                    
                    is_match = self.face_model.calculate_face_distance(encoding, self.encoded_faces, threshold=0.5)
                    if is_match:
                        successful_attempts += 1
                        print(f"Successful attempts {successful_attempts}")
                        if successful_attempts >= 5:
                            print(f"Authenticated as {is_match}")
                            return {"message": f"User authenticated successfully as {is_match}"}
                    else:
                        print("Authentication failed, trying again...")
                    
                time.sleep(0.1)
                    
                if total_attempts == 0:
                    print("Maximum attempts reached.")
                    break
                
                    #Using compare
                    # match = self.face_model.compare_faces(encoding, self.encoded_faces, tolerance=0.5)
                    #if match:
                    #   print("Is match: ", match)  
                    #   successful_attempts += 1
                    #    return {"message": f"User authenticated successfully as {match}"}  
                    #End tests
                               
                    #Actual code to pull stuff from the database  
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

                
                
        except Exception as e:
            print("An error occurred; ", e)
        finally:
            del self.camera_feed
        return {"error": "Authentication failed"}
