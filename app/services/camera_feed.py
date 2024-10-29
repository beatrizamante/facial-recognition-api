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
        rgb_frame = frame[:, :, ::-1]
        
        face_locations = face_recognition.face_locations(rgb_frame)

        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
        
        if not ret:
            raise ValueError("Could not read from camera")
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
    
    def authenticate(self):
        '''Função que faz a autenticação e mantém a câmera aberta até que o usuário seja autenticado.'''
        while not self.is_authenticated:
            frame = self.get_frame()
            cv2.imshow("Camera Feed", frame)

            if cv2.waitKey(1) & 0xFF == ord('1'): #Adicionar um reterno the autenticação correta aqui
                break
        
    def __del__(self):
        '''Função responsável por parar a captura da câmera'''
        self.video_capture.release()
        cv2.destroyAllWindows() 
        