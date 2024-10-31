from fastapi import FastAPI, File, UploadFile
import numpy as np
import cv2
from app.models.face_model import FaceModel

app = FastAPI()

@app.post("/encode")

async def encode_face(image: UploadFile = File(...)):
    '''Função recebe imagem de aplicativo e transforma em uma imagem.
    retorna um encoding'''
    
    image_data = await image.read()
    
    np_img = np.frombuffer(image_data, np.uint8)
    frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    
    face_encodings = FaceModel.extract_face_encoding(frame)
    
    if face_encodings:
        return {"encoding": face_encodings[0].tolist()}
    else:
        return {"error": "No face detected in the image"}
    

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Facial Recognition API"}