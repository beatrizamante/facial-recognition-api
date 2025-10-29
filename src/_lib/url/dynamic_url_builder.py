def build_dynamic_url(group_id: str) -> str:
    '''Constrói o URL da microsoft dinamicamente.
    Parâmetro:
        group_id: Recebe a uid do grupo de usuários.
    Retorna:
        url dinâmica.
    '''
    settings = Settings()
    return f"{settings.BASE_MICROSOFT_URL}/groups/{group_id}/members?$count=true"
