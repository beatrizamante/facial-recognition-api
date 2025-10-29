def detect_faces(frame):
    '''Função responsável por localizar faces na câmera e retornar sua localização
    em real time. Serve para images estáticas também. Recebe uma frame e faz a localização
    do rosto na imagem, retornando as coordenadas em vetor (bottom, left, top, right).'''
    face_locations = face_recognition.face_locations(frame)
    return face_locations

def extract_face_encoding(frame, face_locations):
    '''Função para extração de encoding facial da imagem da câmera.
    Ela recebe uma frame e retorna o encoding do primeiro rosto codificado.'''
    if face_locations:
        encodings = face_recognition.face_encodings(frame, face_locations, num_jitters=2)
        return encodings[0] if encodings else None

def turn_to_encoding(file):
    '''Recebe uma imagem do front e retorna o encoding facial da mesma'''
    file_content = file.file.read()
    image = face_recognition.load_image_file(BytesIO(file_content))
    face_locations = face_recognition.face_locations(image)
    encodings = face_recognition.face_encodings(image, face_locations)
    return encodings
