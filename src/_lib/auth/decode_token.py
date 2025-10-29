def decode_token(auth_token: str) -> str:
    '''Função responsável por decodificar o token de autorização.
    Parâmetros:
        token: recebe o token stored na sessão do browser.
    Retorna:
        A identificação do usuário impressa no token.'''
    if not auth_token:
        raise HTTPException(status_code=400, detail="Token não encontrado")
    try:
        decoded_token = base64.b64decode(auth_token).decode('utf-8')

        return decoded_token

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro ao decodificar token: {e}")
