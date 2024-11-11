import datetime
from fastapi import File, HTTPException, UploadFile, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import pickle   
from app.models.db_get_table import Usuario, SessionLocal
from app.services.auth_services import get_current_user
from app.models.face_model import FaceModel
from app.services.face_services import app

face_model = FaceModel()

class UserModel(BaseModel):
    name: str
    department: str
    user: str
    email: str
    active: bool

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def turn_to_encoding(file): 
    image = face_model.load_image(file)
    face_locations = face_model.detect_faces(image)
    encodings = face_model.extract_face_encoding(image, face_locations)
    return encodings

@app.post("/users", status_code=201, tags=["Users"])
async def create_user(
    user_data: UserModel = Depends(),  
    current_user: str = Depends(get_current_user),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    print("Route /users was hit!")
    try:
        encodings = turn_to_encoding(file)
        if not encodings:
            raise HTTPException(status_code=400, detail="Nenhum rosto detectado.")
        
        encoding = pickle.dumps(encodings[0])

        current_time = datetime.datetime.now()
        new_user = Usuario(
            nome=user_data.name,
            departamento=user_data.department,
            usuario=user_data.user,
            email=user_data.email,
            ativo=user_data.active,
            dataCadastro=current_time,
            usuarioCadastro= current_user,
            hash=encoding
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"status": "Encoding saved", "label": user_data.user}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/user/{user_id}", status_code=200, tags=["UserId"])
async def update_user(
    user_id: int,
    user_data: UserModel = Depends(),
    current_user: str = Depends(get_current_user),
    file: UploadFile = File(None), 
    db: Session = Depends(get_db)
):
    print("Route /user was hit!")
    try:
        existing_user = db.query(Usuario).filter(Usuario.idUsuario == user_id).first()
        if not existing_user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        existing_user.nome = user_data.name
        existing_user.departamento = user_data.department
        existing_user.usuario = user_data.user
        existing_user.email = user_data.email
        existing_user.ativo = user_data.active
        existing_user.usuarioAlteracao = current_user
        existing_user.dataAlteracao = datetime.datetime.now()

        if file:
            encodings = turn_to_encoding(file)
            if not encodings:
                raise HTTPException(status_code=400, detail="Nenhum rosto detectado na imagem.")
            existing_user.hash = pickle.dumps(encodings[0])

        db.commit()
        db.refresh(existing_user)

        return {"status": "Usuário atualizado com sucesso", "nome": user_data.name}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
