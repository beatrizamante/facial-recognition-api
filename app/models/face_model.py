import face_recognition
import cv2
import json

class FaceModel:
    '''Classe responsável pelo service de reconhecimento'''
    
    def extract_face_encoding(self, frame, face_locations):
        '''Função para extração de encoding facial da imagem da câmera. 
        Ela recebe uma frame e retorna o encoding do primeiro rosto codificado.'''
        if face_locations:
            encodings = face_recognition.face_encodings(frame, face_locations, num_jitters=2)
            return encodings[0] if encodings else None
        
    def detect_faces(self, frame):
        '''Função responsável por localizar faces na câmera e retornar sua localização
        em real time. Serve para images estáticas também'''
        face_locations = face_recognition.face_locations(frame)
        return face_locations

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
        um set de codificações já pré-existentes, assim como a que está 
        sendo codificada agora e a tolerância esperada entre ela e retorna o valor 
        de comparação.'''            
        for entry in encoded_faces:
            label = entry['label']
            stored_encode = entry['encoding']
            distance = face_recognition.face_distance([stored_encode], new_encoding)[0]
            print(f"Distance: ", distance)
            if distance < threshold: 
                return label, True  
        return None, False
    
    def get_label(self, encoding, encoded_faces):
        '''Função responsável por extrair o label das encodings.
        Recebe o encoding do usuario atual e os encodings para comparação
        e retorna o label do usuário.'''
        user_label = self.calculate_face_distance(encoding, encoded_faces, threshold=0.5) 
        return user_label if user_label else "Unknown"
    
    def format_to_json(self, encoding):
        '''Função que torna o encoding em um objeto JSON,
        Recebe como parâmetro um encoding e retorna o objeto JSON
        em uma lista'''
        return json.dumps({"encoding": encoding.tolist()})
    
    def draw_boxes(self, frame, face_locations, user_label):
        '''Função desenha retângulos com o nome da pessoa quando está é
        reconhecida pelo software. Recebe o frame e o usuário em questão e
        retorna o frame com o box.'''
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, user_label, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            
    def convert_to_rgb(self, frame):
        '''Função para ajustar frames recebidas para tipo de imagem que 
        o facial-recognition reconhece e retorna o formato correto. Recebe uma frame
        e retorna a frame convertida para rgb.'''
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        return rgb_frame
