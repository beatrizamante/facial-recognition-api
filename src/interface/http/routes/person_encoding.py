router = APIRouter()

@router.post("/gerarEnconding", status_code=201, tags=["Generate encoding"])
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
