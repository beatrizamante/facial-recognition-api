import base64
from typing import Dict
from fastapi import HTTPException, requests, status
from dotenv import load_dotenv

load_dotenv()

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
    

def decode_token(auth_token: str) -> str:
    '''Função responsável por decodificar o token de autorização.
    Parâmetros: 
        token: recebe o token stored na sessão do browser.
    Retorna: 
        A identificação do usuário impressa no token.'''
    if not auth_token:
        return None
        # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token não encontrado")
    try:
        decoded_token = base64.b64decode(auth_token).decode('utf-8')   
        
        print(f"Payload______________________{decoded_token}")
        return decoded_token
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro ao decodificar token: {e}")

def build_dynamic_url(group_id: str) -> str:
    '''Constrói o URL da microsoft dinamicamente.
    Parâmetro:
        group_id: Recebe a uid do grupo de usuários.
    Retorna:
        url dinâmica.
    '''
    base_url = "https://graph.microsoft,com/v1.0"
    url = f"{base_url}/groups/{group_id}/members?$count=true"
    return url

async def fetch_group_members(token: str, group_id: str):
    '''Recupera o group_id através do token.
    Parâmetros: 
        token: token recebido no payload
    Retorna:
        O grupo de membros da lista para comparação com o email.
    '''
    url = build_dynamic_url(group_id)
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        members = response.json().get('value', [])
        mails = [member.get("mail") for member in members if 'mail' in member]
        return mails
    
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Erro ao acessar membros: {response.status_code}, {response.text}")

