router = APIRouter()

router.mount("/static", StaticFiles(directory="static"), name="static")

@router.get("/")
async def get_index():
    """Redireciona para o index.html. O index.html é uma página com câmera
    apenas para testes - caso seja necessário no futuro que o programa desenhe
    retângulos no rosto dos usuários e retorne o nome destes assim que a biometria
    os reconhecer, basta pegar a lógica do script.js."""
    return RedirectResponse(url="/static/index.html")
