from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import logging
from app.services.face_services import app

#________________________
import datetime
from fastapi import File, HTTPException, Request, UploadFile, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import pickle   
from app.models.db_table_sqlalc import Usuario
from app.services.face_services import app
from app.utils.db_get import get_db
from app.utils.get_current_user import get_current_user
from app.utils.load_image import turn_to_encoding
from typing import List

#_____________________________________

#Log de erros pront para uso caso seja necessário
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(message)s")
logger = logging.getLogger("uvicorn")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def get_index():
    """Redireciona para o index.html. O index.html é uma página com câmera 
    apenas para testes - caso seja necessário no futuro que o programa desenhe
    retângulos no rosto dos usuários e retorne o nome destes assim que a biometria
    os reconhecer, basta pegar a lógica do script.js."""
    return RedirectResponse(url="/static/index.html")

if __name__ == "__main__":
    config = uvicorn.Config("main:app", 
                            host="0.0.0.0", 
                            port=443, 
                            ssl_certfile="./agrariacoopbr.cert",
                            ssl_keyfile="./agrariacoopbr.key"
                            )
    server = uvicorn.Server(config)
    server.run()
    
    
    #_______________________________________

class UserModel(BaseModel):
    '''Classe Modelo de validações de um usuário no banco de dados'''
    name: str
    department: str
    user: str
    email: str
    active: bool
    class Config:
        orm_mode = True
        
@app.get("/users", status_code=200, tags=["Retrieve All Users"])
async def get_all_users(db: Session = Depends(get_db)):
    '''Função método get para retornar informações gerais de todos os usuários.
    Parâmetros: 
        db: instância de conexão com o banco por conta do sqlalchemy.
    Retorna: 
        Retorna todas as informações de todos os usuários salvas no banco, com exceção do hash, 
        que será só acessado por backend por motivos de segurança.
        '''
    try:
        users = db.query(Usuario).all()
        users_data = [
            {key: value for key, value in user.__dict__.items() if key not in ["hash", "hash1"]} for user in users
        ]
        return users_data
 
    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
 
 
@app.get("/user/{user_id}", status_code=200, tags=["Retrieve One User"])
async def get_user_by_id(user_id: int,
                         db: Session = Depends(get_db)):
    '''Função método get para retornar informações gerais de um usuário específico.
    Parâmetros: 
        id_user: Id do usuário a ser encontrado,
        db: instância de conexão com o banco por conta do sqlalchemy.
    Retorna: 
        Retorna todas as informações de um usuário salvas no banco com exceção do hash, 
        que será só acessado por backend por motivos de segurança.
    '''
 
    try:
        user = db.query(Usuario).filter(Usuario.id == user_id).first()
        if not user:
            raise HTTPException(status_code=400, detail="Usuário não encontrado")
        user_data =  {key: (value if key not in ["hash", "hash1"] else None) for key, value in user.__dict__.items()} 
        
        return user_data
 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 

@app.post("/users", status_code=201, tags=["Create User"])
async def create_user(
    user_data: UserModel = Depends(),  
    current_user: str = Depends(get_current_user),
    file1: List[UploadFile] = File(...),
    file2: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    '''Função método post para criar um usuário no banco de dados
    Parâmetros: 
        user_data: recebe o modelo de validação do usuário do Pydantic para chamar as informações corretas do form no front,
        current_user: o usuário quem está fazendo a adição,
        file1: imagem provindo da usuário para configuração,
        file2: imagem provindo da usuário para configuração, ambas são necessárias,
        db: instância de conexão com o banco por conta do sqlalchemy.
    Retorna:
        Resposta positiva e label da pessoa que foi alterada caso tenha commitado corretamente no banco,
        ou dá Raise Error caso algum erro aconteça.'''
 
    try:
     
        files = file1 + file2
        user_encodings = []
     
        for file in files:
            encodings = turn_to_encoding(file)
            if not encodings:
                raise HTTPException(status_code=400, detail="Nenhum rosto detectado, favor, trocar imagem.")
        
            encoded_binary = pickle.dumps(encodings[0])
            user_encodings.append(encoded_binary)
     
        new_user = Usuario(
            nome=user_data.name,
            departamento=user_data.department,
            matricula=user_data.user,
            email=user_data.email,
            ativo=user_data.active,
            dataCadastro=datetime.datetime.now(),
            usuarioCadastro=current_user,
            hash=user_encodings[0],
            hash1=user_encodings[1]
        )
     
        db.add(new_user)
        try:
            db.commit()
        except Exception as e:
            db.rollback()  
            print(f"Error during commit: {e}")
            raise HTTPException(status_code=500, detail="Database error")
        db.refresh(new_user)
        return {"status": "Usuário salvo", "label": new_user.matricula}
 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.put("/user/{user_id}", status_code=200, tags=["Update User"])
async def update_user(
    user_id: int,
    request: Request,
    user_data: UserModel = Depends(),
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    '''Classe responsável por fazer o upload de informações do usuário por método put.
    Parâmetros: 
        id_user: Id do usuário a ser alterado,
        request: Request body para recuparação de "file" de dentro deste,
        user_data: recebe o modelo de validação do usuário do Pydantic para chamar as informações corretas do form no front,
        current_user: o usuário quem está fazendo a alteração,
        db: instância de conexão com o banco por conta do sqlalchemy.
    Retorna:
        Resposta positiva e label da pessoa que foi alterada caso tenha commitado corretamente no banco,
        ou dá Raise Error caso algum erro aconteça.'''
 
    try:
        existing_user = db.query(Usuario).filter(Usuario.id == user_id).first()
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
     
        form = await request.form()
        files = ["file1", "file2"]
        encodings = []
        
        for file_key in files:
            if file_key in form:
                file = form[file_key]
                if file:
                    encoding = turn_to_encoding(file)
                    turn_binary = pickle.dumps(encoding)
                    if not encoding:
                        raise HTTPException(status_code=400, detail=f"Nenhum rosto detectado na imagem {file_key}.")
                    encodings.append(turn_binary)  
        
        if encodings:
            if len(encodings) > 0:
                existing_user.hash = encodings[0]
            if len(encodings) > 1:
                existing_user.hash1 = encodings[1]
             
        try:
            db.commit()
        except Exception as e:
            db.rollback()  
            print(f"Error during commit: {e}")
            raise HTTPException(status_code=500, detail="Database error")
        db.refresh(existing_user)
        return {"status": "Usuário atualizado com sucesso", "label": user_data.name}
 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))