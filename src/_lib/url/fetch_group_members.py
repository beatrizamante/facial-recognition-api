async def fetch_group_members(token: str, group_id: str):
    '''Recupera o group_id através do token.
    Parâmetros:
        token: token recebido no payload
    Retorna:
        O grupo de membros da lista para comparação com o email.
    '''
    url = build_dynamic_url(group_id)

    response = requests.get(url, headers={'Authorization': f'Bearer {token}'})

    if response.status_code == 200:
        members = response.json().get('value', [])
        mails = [member.get("mail") for member in members if 'mail' in member]
        return mails

    raise HTTPException(status_code=response.status_code, detail=f"Erro ao acessar membros: {response.status_code}, {response.text}")
