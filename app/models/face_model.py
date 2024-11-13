import pickle
import face_recognition
import cv2
import json
import numpy as np

class FaceModel:
    '''Classe responsável pelo service de reconhecimento. Para todos os items que usam
    face_recognition, o tipo de imagem que a api aceita é em fortmato rgb, então se for
    usar algo que necessite do mesmo, favor usar covert_to_rgb antes.'''
    
    def convert_to_rgb(self, frame):
        '''Função para ajustar frames recebidas para tipo de imagem que 
        o facial-recognition reconhece e retorna o formato correto. Recebe uma frame
        e retorna a frame convertida para rgb.'''
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        return rgb_frame
    
    def detect_faces(self, frame):
        '''Função responsável por localizar faces na câmera e retornar sua localização
        em real time. Serve para images estáticas também. Recebe uma frame e faz a localização
        do rosto na imagem, retornando as coordenadas em vetor.'''
        face_locations = face_recognition.face_locations(frame)
        return face_locations
    
    def extract_face_encoding(self, frame, face_locations):
        '''Função para extração de encoding facial da imagem da câmera. 
        Ela recebe uma frame e retorna o encoding do primeiro rosto codificado.'''
        if face_locations:
            encodings = face_recognition.face_encodings(frame, face_locations, num_jitters=2)
            return encodings[0] if encodings else None
        
    # def compare_faces(self, new_encoding, encoded_faces, tolerance=0.5):
    #     '''Função responsável por comparar as faces codificadas em um array com a 
    #     recebida pelo frame. Recebe um ndarray de encodes, assim como a frame codificada
    #     atual e também a tolerância base (learning rate) para comparação, retorna
    #     o True se encotrar um match, ou falso se não encontrar. NO MOMENTO NÃO
    #     ESTÁ SENDO USADA.'''
    #     for entry in encoded_faces: 
    #         label = entry['label']
    #         stored_encode = entry['encoding'] 
    #         matches = face_recognition.compare_faces([stored_encode], new_encoding, tolerance)
    #         if matches[0]:
    #             return label
    #     return None


    def calculate_face_distance(self, new_encoding, encoded_faces, threshold):
        '''Função responspavel por fazer o calculo de proximidade entre as faces
        do banco de dados com a que está sendo recebida pela programa, recebe
        um set de codificações já pré-existentes, assim como a que está 
        sendo codificada agora e a tolerância esperada entre ela e retorna 
        o label da pessoa do banco e se essa bate com o valor no banco com 
        um boolean.'''  
        for entry in encoded_faces:
            label = entry['label']
            mail = entry['mail']
            stored_encode = [np.array(encoding) for encoding in entry['encoding']]
            
            print(f"Two hashes___________________________{stored_encode}")
            
            distances = face_recognition.face_distance(stored_encode, new_encoding)
            
            print(f"Distances____________________{distances}")
            print(f"Threshold____________________{threshold}")
            
            if distances[0] < threshold and distances[1] < threshold:
                print("Enters if_______________________")
                
                print(f"Both distances are a match for {label}, {mail}")
                return label, mail, True
              
        return None, None, False
    

        