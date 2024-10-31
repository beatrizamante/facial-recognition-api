'''Módulo responsável por capturar frames da câmera'''

import cv2
import face_recognition
from app.models.face_model import FaceModel
class CameraFeed:
    '''Classe de captura'''
    def __init__(self):
        self.face_model = FaceModel()
        self.video_capture = cv2.VideoCapture(0)
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set width
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
    def get_frame(self):
        '''Função que inicia a captura dos frames, retornando o frame atual
        e a localicação das faces em câmera.
        Recebe uma label como parâmetro para adicionar nos retângulos.'''
        
        frame_count = 0
        while True:
            ret, frame = self.video_capture.read()
            if not ret or frame is None:
                raise ValueError("Could not read from camera")
            
            if frame_count % 15 == 0:
                processed_frame, face_locations = self.process_frame(frame)
                yield processed_frame, face_locations
            else:
                yield frame, []

            self.face_model.draw_boxes(frame, face_locations, user_label="")
            cv2.imshow("Camera Feed", frame)
        
            frame_count += 1
            if cv2.waitKey(1) & 0xFF == 27:  # ESC key
                break
            
    def process_frame(self, frame):
        '''Função responsável por processar a frame recebida para comparação,
        diminuindo assim o processamento. Recebe uma frame e retorna a frame 
        processada.'''
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        
        adjusted_locations = [(int(top * 2), int(right * 2), int(bottom * 2), int(left *2))
                              for(top, right, bottom, left) in face_locations]
        
        return frame, adjusted_locations
    
    def __del__(self):
        '''Libera a camera e deleta todas as janelas quando chamado.'''
        if self.video_capture is not None:
            self.video_capture.release()
            cv2.destroyAllWindows()
            self.video_capture = None

    

        