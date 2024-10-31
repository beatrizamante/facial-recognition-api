'''Módulo responsável por capturar frames da câmera'''

import time
import cv2
import face_recognition

class CameraFeedThread:
    '''Classe de captura'''
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.running = True
        self.frame = None
        self.face_locations = []
        
    def capture_frame(self):
        '''Captura frames da câmera num thread separado para melhorar
        o desempenho do código.'''
        while self.running: 
            ret, frame = self.video_capture.read()
            if not ret:
                raise ValueError("Could not read from camera")
            self.frame = frame
            time.sleep(0.01)
        
    def get_frame(self):
        '''Função retorna o frame atual e a localicação das faces em câmera.'''
        
        if self.frame is None:
            return None, []
        
        small_frame = cv2.resize(self.frame, (0, 0), fx=0.5, fy=0.5)
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        self.face_locations = face_recognition.face_locations(rgb_frame)
    
    def stop_camera(self):
        '''Libera a camera e deleta todas as janelas quando chamado.'''
        self.running = False        
        self.video_capture.release()
        cv2.destroyAllWindows()

    

        