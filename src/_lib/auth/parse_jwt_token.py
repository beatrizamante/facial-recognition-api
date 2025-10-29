async def parse_token(header: str) -> Dict[str, str]:
    '''Extrai o token e o group_id do Websocket header.
        Parâmetros:
            header: WebSocket 'sec.websocket-protocol' header value.
        Retorno:
            Um dicionário contendo auth_token e group_token.
    '''
    try:
        tokens = header.split(",")
        return {
            "auth_token": tokens[0],
            "group_token": tokens[1] if len(tokens) > 1 else None
        }

    except IndexError:
        raise ValueError("Header de formato inválido")
