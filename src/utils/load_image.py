

from io import BytesIO
import face_recognition

def turn_to_encoding(file): 
    '''Recebe uma imagem do front e retorna o encoding facial da mesma'''
    file_content = file.file.read()
    image = face_recognition.load_image_file(BytesIO(file_content))
    face_locations = face_recognition.face_locations(image)
    encodings = face_recognition.face_encodings(image, face_locations)
    return encodings