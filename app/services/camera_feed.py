'''Módulo responsável por capturar frames da câmera'''

import json
import cv2
import face_recognition
from app.utils.helpers import resizing

class CameraFeed:
    '''Classe de captura'''
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        
    def get_frame(self):
        '''Função que inicia a captura dos frames, retornando o frame atual'''
        ret, frame = self.video_capture.read()     
        self.draw_boxes(frame)
        if not ret or frame is None:
            raise ValueError("Could not read from camera")
        return frame
    
    
    def draw_boxes(self, frame, user_label=""):
        '''Função desenha retângulos com o nome da pessoa quando está é
        reconhecida pelo software. Recebe o frame e o usuário em questão e
        reorna o frame com o box.'''
        
        process_this_frame = True
        if process_this_frame:
            rgb_frame = frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_frame)
            
            process_this_frame = not process_this_frame
            
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, user_label, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            return frame
        

    def format_to_json(self, encoding):
        '''Função que torna o encoding em um objeto JSON,
        Recebe como parâmetro um encoding e retorna o objeto JSON
        em uma lista'''
        return json.dumps({"encoding": encoding.tolist()})
    
    def display_feed(self):
        '''Método que exibe o feed da câmera em uma janela OpenCV para testar no notebook.'''
        while True:
            frame = self.get_frame() 
            cv2.imshow("Camera Feed", frame)  

            if cv2.waitKey(1) & 0xFF == 27:  # ESC key
                break
        
    def __del__(self):
        '''Função responsável por parar a captura da câmera'''
        self.video_capture.release()
        cv2.destroyAllWindows() 
        