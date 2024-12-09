from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import logging
from app.services.face_services import app

#____________________________________
#Deixando esses no main até pensar numa forma melhor de usá-los, possivelmente em user_services
from fastapi import File, HTTPException, UploadFile
from app.services.face_services import app
from app.utils.load_image import turn_to_encoding
from typing import List
from app.utils.turn_to_base64 import encode_to_base64
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
@app.post("/gerarEnconding", status_code=201, tags=["Generate encoding"])
async def generate_enconding(
    file1: List[UploadFile] = File(...),
    file2: List[UploadFile] = File(...),
):
    '''Função método post para tornar imagems em encodings e enviar para a api para o banco de dados
    Parâmetros: 
        file1: imagem provindo da usuário para configuração,
        file2: imagem provindo da usuário para configuração, ambas são necessárias,
    Retorna:
        Encodings de ambas as imagems com suas respectivas respostas na API.'''
 
    try:
        files = file1 + file2
        user_encodings = []
        for file in files:
            encodings = turn_to_encoding(file)
            if not encodings:
                raise HTTPException(status_code=400, detail="Nenhum rosto detectado, favor, trocar imagem.")
            encoded_binary = encode_to_base64(encodings[0])
            user_encodings.append(encoded_binary)
     
        return {"hash1": user_encodings[0], "has2": user_encodings[1]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
