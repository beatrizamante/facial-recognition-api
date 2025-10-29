router = APIRouter()


router.mount("/static", StaticFiles(directory="static"), name="static")

@router.get("/")
async def get_index():
    return RedirectResponse(url="/static/index.html")
