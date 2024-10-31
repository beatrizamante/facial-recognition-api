import requests
from app.services.camera_feed import CameraFeed
from app.models.face_model import FaceModel

class FaceControllerJson:
    '''Classe responsável pelo service de reconhecimento'''
    def __init__(self):
        self.face_model = FaceModel()
        self.camera_feed = CameraFeed()
    
    async def send_encodes_json_backend(self, backend_url):
        '''Pega as frames e envia para o backend para comparação.
        Recebe a url do backend como pâemetro e empacota o encoding
        facia em objeto json. Se a resposta do back for 200, autentica com 
        sucesso. Loga depois de 5 tentativas com sucesso. Se não, levanta erro'''

        user_label = "Identifying..."
        successful_attempts = 0
        total_attempts = 80

        try:
            for frame, face_locations in self.camera_feed.get_frame():
                total_attempts -= 1

                if face_locations:
                    encoding = self.face_model.extract_face_encoding(frame, face_locations)
                else:
                    encoding = None

                if encoding is not None:
                    json_data = self.face_model.format_to_json(encoding)

                    response = requests.post(backend_url, data=json_data,
                                             headers={"Content-Type": "application/json"})

                    if response.status_code == 200:
                        response_data = response.json()
                        user_label = response_data.get("user_id", "name")
                        successful_attempts += 1
                        if successful_attempts >= 5:
                            return {"message": f"User authenticated successfully as {user_label}"}
                    else:
                        print("Authentication failed, trying again...")

                if total_attempts == 0:
                    print("Maximum attempts reached.")
                    break
                
        except Exception as e:
            print("An error occurred:", e)
        finally:
            del self.camera_feed
        return {"error": "Authentication failed"}


        