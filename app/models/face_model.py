import face_recognition

class FaceModel:
    '''Classe responsável pelo service de reconhecimento'''
    
    def extract_face_encoding(self, frame, face_locations):
        '''Função para extração de encoding facial da imagem da câmera. 
        Ela recebe uma frame e retorna o encoding do primeiro rosto codificado.'''
        if face_locations:
            encodings = face_recognition.face_encodings(frame, face_locations, num_jitters=2)
            if not encodings:
                return None
            return encodings[0]

    def compare_faces(self, new_encoding, encoded_faces, tolerance=0.6):
        '''Função responsável por comparar as faces codificadas em um array com a 
        recebida pelo frame. Recebe um ndarray de encodes, assim como a frame codificada
        atual e também a tolerância base (learning rate) para comparação, retorna
        o True se encotrar um match, ou falso se não encontrar.'''
        for entry in encoded_faces: 
            label = entry['label']
            stored_encode = entry['encoding']        
            matches = face_recognition.compare_faces([stored_encode], new_encoding, tolerance)
            if matches[0]:
                return label
        return None

    def calculate_face_distance(self, known_encodings, new_encodings):
        '''Função responspavel por fazer o calculo de proximidade entre as faces
        do banco de dados com a que está sendo recebida pela programa, recebe
        um set de codificaçẽos já pré-existentes, assim como a que está 
        sendo codificada agora e a tolerância esperada entre ela e retorna o valor 
        de comparação.'''
        for entry in known_encodings: 
            label = entry['label']
            stored_encode = entry['encoding']    
            distances = face_recognition.face_distance(stored_encode, new_encodings)
            match_found = any(distance < 0.4 for distance in distances)
            
            if match_found:
                return label
        return None