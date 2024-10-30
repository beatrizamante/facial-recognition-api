'''Módulo responsável por capturar frames da câmera'''

import json
import cv2
import face_recognition
from app.models.face_model import FaceModel
class CameraFeed:
    '''Classe de captura'''
    def __init__(self):
        self.face_model = FaceModel()
        self.video_capture = None
        
    def get_frame(self):
        '''Função que inicia a captura dos frames, retornando o frame atual'''
        self.video_capture = cv2.VideoCapture(0)
        
        process_this_frame = True
        
        while True:
            ret, frame = self.video_capture.read()
            if not ret or frame is None:
                raise ValueError("Could not read from camera")
            
            if process_this_frame:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = self.face_model.extract_face_encoding(rgb_frame, face_locations)
                print("Encodings: ", face_encodings)
            
            process_this_frame = not process_this_frame
            self.draw_boxes(frame, face_locations)


            cv2.imshow("Camera Feed", frame)

            if cv2.waitKey(1) & 0xFF == 27:  # ESC key
                break

        self.video_capture.release()
        cv2.destroyAllWindows()
    
    
    def draw_boxes(self, frame, face_locations, user_label=""):
        '''Função desenha retângulos com o nome da pessoa quando está é
        reconhecida pelo software. Recebe o frame e o usuário em questão e
        retorna o frame com o box.'''
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, "user_label", (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            
            return frame
    

    def format_to_json(self, encoding):
        '''Função que torna o encoding em um objeto JSON,
        Recebe como parâmetro um encoding e retorna o objeto JSON
        em uma lista'''
        return json.dumps({"encoding": encoding.tolist()})

        