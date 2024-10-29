'''Módulo responsável por capturar frames da câmera'''

import json
from cv2 import cv2
from app.utils.helpers import resizing

class CameraFeed:
    '''Classe de captura'''
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        
    def get_frame(self):
        '''Função que inicia a captura dos frames, retornando o frame atual'''
        ret, frame = self.video_capture.read()
        resizing(frame)
        
        if not ret:
            raise ValueError("Could not read from camera")
        return frame
        

    def format_to_json(self, encoding):
        '''Função que torna o encoding em um objeto JSON,
        Recebe como parâmetro um encoding e retorna o objeto JSON
        em uma lista'''
        return json.dumps({"encoding": encoding.tolist()})
    
    def __del__(self):
        '''Função responsável por parar a captura da câmera'''
        self.video_capture.release()
        