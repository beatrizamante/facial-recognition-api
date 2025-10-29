import json
import time

class FaceController:
    '''Classe responsável pelo service de reconhecimento'''
    def __init__(self):
        with open("encoded_faces.json", "r", encoding='utf-8') as f:
            self.encoded_faces = json.load(f)

    def authenticate_user_clientside(self):
        '''Função responsável por capturar frames e enviar encodings faciais
        até que o usuário seja autenticado.'''

        successful_attempts = 0
        total_attempts = 300

        try:
            for frame, face_locations in get_frame():
                total_attempts -= 1
                if face_locations:
                    encoding = extract_face_encoding(frame, face_locations)
                    if encoding is not None:
                        label, is_match = calculate_face_distance(encoding, self.encoded_faces, threshold=0.5)
                        if is_match:
                            successful_attempts += 1
                            if successful_attempts >= 5:
                                print(f"Authenticated with {label}")
                                return {"message": f"User authenticated successfully as {label}"}
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
            del camera_feed
