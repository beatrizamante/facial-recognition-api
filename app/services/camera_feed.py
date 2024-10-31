'''Módulo responsável por capturar frames da câmera'''

import json
import cv2
import face_recognition
from app.models.face_model import FaceModel
class CameraFeed:
    '''Classe de captura'''
    def __init__(self):
        self.face_model = FaceModel()
        self.video_capture = cv2.VideoCapture(0)
        
    def get_frame(self, user_label):
        '''Função que inicia a captura dos frames, retornando o frame atual
        e a localicação das faces em câmera.
        Recebe uma label como parâmetro para adicionar nos retângulos.'''
        
        frame_count = 0
        while True:
            ret, frame = self.video_capture.read()
            if not ret or frame is None:
                raise ValueError("Could not read from camera")
            
            if frame_count % 10 == 0:
                rgb_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame)
                yield frame, face_locations
            else:
                yield frame, []
            
            self.draw_boxes(frame, face_locations, user_label="")
            cv2.imshow("Camera Feed", frame)
        
            frame_count += 1
            if cv2.waitKey(1) & 0xFF == 27:  # ESC key
                break
    
    def draw_boxes(self, frame, face_locations, user_label=""):
        '''Função desenha retângulos com o nome da pessoa quando está é
        reconhecida pelo software. Recebe o frame e o usuário em questão e
        retorna o frame com o box.'''
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, user_label, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    
    def __del__(self):
        '''Libera a camera e deleta todas as janelas quando chamado.'''
        if self.video_capture is not None:
            self.video_capture.release()
            cv2.destroyAllWindows()
            self.video_capture = None

    def format_to_json(self, encoding):
        '''Função que torna o encoding em um objeto JSON,
        Recebe como parâmetro um encoding e retorna o objeto JSON
        em uma lista'''
        return json.dumps({"encoding": encoding.tolist()})

        