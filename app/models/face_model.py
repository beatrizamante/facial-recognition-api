import face_recognition
import json

class FaceModel:
    '''Classe responsável pelo service de reconhecimento'''
    
    def extract_face_encoding(self, frame, face_locations):
        '''Função para extração de encoding facial da imagem da câmera. 
        Ela recebe uma frame e retorna o encoding do primeiro rosto codificado.'''
        if face_locations:
            encodings = face_recognition.face_encodings(frame, face_locations, num_jitters=2)
            return encodings[0] if encodings else None

    def compare_faces(self, new_encoding, encoded_faces, tolerance=0.5):
        '''Função responsável por comparar as faces codificadas em um array com a 
        recebida pelo frame. Recebe um ndarray de encodes, assim como a frame codificada
        atual e também a tolerância base (learning rate) para comparação, retorna
        o True se encotrar um match, ou falso se não encontrar.'''
        for entry in encoded_faces: 
            label = entry['label']
            stored_encode = entry['encoding'] 
            print(f"Label: {label}, enconding: {stored_encode}")       
            matches = face_recognition.compare_faces([stored_encode], new_encoding, tolerance)
            if matches[0]:
                return label
        return None

    def calculate_face_distance(self, new_encoding, encoded_faces, threshold):
        '''Função responspavel por fazer o calculo de proximidade entre as faces
        do banco de dados com a que está sendo recebida pela programa, recebe
        um set de codificaçẽos já pré-existentes, assim como a que está 
        sendo codificada agora e a tolerância esperada entre ela e retorna o valor 
        de comparação.'''            
        for entry in encoded_faces:
            label = entry['label']
            stored_encode = entry['encoding']
            distance = face_recognition.face_distance([stored_encode], new_encoding)[0]
            if distance < threshold: 
                return label  
        return None
    
    def get_label(self, encoding, encoded_faces):
        '''Função callback para devolver um label para os 
        retângulos desenhados no rosto do usuário. Recebe um label
        e retorna ele para a outra função'''
        user_label = self.calculate_face_distance(encoding, encoded_faces, threshold=0.5) 
        return user_label if user_label else "Unknown"
    
    def format_to_json(self, encoding):
        '''Função que torna o encoding em um objeto JSON,
        Recebe como parâmetro um encoding e retorna o objeto JSON
        em uma lista'''
        return json.dumps({"encoding": encoding.tolist()})
