'''Módulo utilizado para processar a imagem da câmera do usuário
utilizando do facial-recognition'''

import face_recognition
class FaceRecognitionService:
    '''Classe responsável pelo service de reconhecimento'''
    
    def extract_face_encoding(self, frame):
        '''Função para extração de encoding facial da imagem da câmera. 
        Ela recebe uma frame e retorna o encoding do primeiro rosto encodado.'''
        
        face_locations = face_recognition.face_locations(frame)
        if face_locations:
            return face_recognition.face_encodings(frame, face_locations)[0]
        return None
    
    def compare_faces(self, known_encoding, unknown_encoding, tolerance=0.6):
        '''Função responsável por comparar as faces codificadas em um array com a 
        recebida pelo frame. Recebe um ndarray de encodes, assim como a frame codificada
        atual e também a tolerância base (learning rate) para comparação, retorna
        o resultado da comparação.'''
        return face_recognition.compare_faces([known_encoding],
                                              unknown_encoding, tolerance=tolerance)[0]
        
    def calculate_face_distance(self, known_encoding, unknown_encoding):
        '''Função responspavel por fazer o calculo de proximidade entre as faces
        do banco de dados com a que está sendo recebida pela programa, recebe
        um set de codificaçẽos já pré-existentes, assim como a que está 
        sendo codificada agora e a tolerância esperada entre ela e retorna o valor 
        de comparação.'''
        
        return face_recognition.face_distance([known_encoding, unknown_encoding], unknown_encoding)[0]
        
