import datetime
from typing import Optional
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import logging
from app.services.face_services import app

#___import datetime
from fastapi import File, HTTPException, UploadFile, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import pickle   
from app.models.db_get_table import Usuario
from app.utils.get_current_user import get_current_user
from app.utils.db_get import get_db
from app.utils.load_image import turn_to_encoding
#_______________

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(message)s")
logger = logging.getLogger("uvicorn")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def get_index():
    """Redirect to index.html in the static folder. THIS IS FOR TESTING ONLY"""
    return RedirectResponse(url="/app/static/index.html")

if __name__ == "__main__":
    config = uvicorn.Config("main:app", 
                            host="0.0.0.0", 
                            port=443, 
                            ssl_certfile="./agrariacoopbr.cert",
                            ssl_keyfile="./agrariacoopbr.key"
                            )
    server = uvicorn.Server(config)
    server.run()
    
#Iniciando post e put aqui pra testar no insomnia
class UserModel(BaseModel):
    name: str
    department: str
    user: str
    email: str
    active: bool

    class Config:
        orm_mode = True

@app.post("/users", status_code=201, tags=["Create User"])
async def create_user(
    user_data: UserModel = Depends(),  
    current_user: str = Depends(get_current_user),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    '''Função método post para criar um usuário no banco de dados
    recebe o user_data que é o input do usuário feito no front seguindo
    o formato UserModel, o usuário que está fazendo o cadastro, a imagem
    que está sendo carregada e a conexão com o banco e retorna uma resposta
    positiva caso o processo tenha sido efetuado com sucesso.'''
    
    try:
        encodings = turn_to_encoding(file)
        if not encodings:
            raise HTTPException(status_code=400, detail="Nenhum rosto detectado.")
        
        encoding = pickle.dumps(encodings[0])

        new_user = Usuario(
            nome=user_data.name,
            departamento=user_data.department,
            matricula=user_data.user,
            email=user_data.email,
            ativo=user_data.active,
            dataCadastro=datetime.datetime.now(),
            usuarioCadastro=current_user,
            hash=encoding
        )

        print(f"New user added {new_user}")
        db.add(new_user)
        try:
            db.commit()
            print("Committed user to DB") 
        except Exception as e:
            db.rollback()  
            print(f"Error during commit: {e}")
            raise HTTPException(status_code=500, detail="Database error")
        db.refresh(new_user)

        return {"status": "Encoding saved", "label": new_user.matricula}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/user/{user_id}", status_code=200, tags=["Update User"])
async def update_user(
    user_id: int,
    user_data: UserModel = Depends(),
    current_user: str = Depends(get_current_user),
    file: Optional[UploadFile] = File(None), 
    db: Session = Depends(get_db)
):
    try:
        existing_user = db.query(Usuario).filter(Usuario.idUsuario == user_id).first()
        if not existing_user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        if user_data.name:
            existing_user.nome = user_data.name
        if user_data.department:
            existing_user.departamento = user_data.department
        if user_data.user:
            existing_user.matricula = user_data.user
        if user_data.email:
            existing_user.email = user_data.email 

        existing_user.usuarioAlteracao = current_user
        existing_user.dataAlteracao = datetime.datetime.now()
        
   
        #Still not working if file is empty
        if file and isinstance(file, UploadFile):
            encodings = turn_to_encoding(file)
            if not encodings:
                raise HTTPException(status_code=400, detail="Nenhum rosto detectado na imagem.")
            existing_user.hash = pickle.dumps(encodings[0])

        try:
            db.commit()
            print("Committed user to DB") 
        except Exception as e:
            db.rollback()  
            print(f"Error during commit: {e}")
            raise HTTPException(status_code=500, detail="Database error")
        db.refresh(existing_user)

        return {"status": "Usuário atualizado com sucesso", "nome": user_data.name}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users", status_code=200, tags=["Retrieve All Users"])
async def get_all_users(db: Session = Depends(get_db)):
    try:
        users = db.query(Usuario).all()
        users_data = [
            {key: value for key, value in user.__dict__.items() if key != "hash"} for user in users
        ]
        return users_data
    
    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    
@app.get("/user/{user_id}", status_code=200, tags=["Retrieve One User"])
async def get_user_by_id(user_id: int,
                         db: Session = Depends(get_db)):
    try:
        user = db.query(Usuario).filter(Usuario.idUsuario == user_id).first()
        if not user:
            raise HTTPException(status_code=400, detail="Usuário não encontrado")

        user_data =  {key: (value if key != 'hash' else None) for key, value in user.__dict__.items()} 
        return user_data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#--------------

@app.get("/print-users", status_code=200, tags=["Users"])
async def print_users(db: Session = Depends(get_db)):
    try:
        # Query all users
        users = db.query(Usuario).all()
        
        users_data = [
            {key: (value if key != 'hash' else None) for key, value in user.__dict__.items()}
            for user in users
        ]
        
        return users_data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 