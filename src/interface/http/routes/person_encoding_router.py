router = APIRouter()

@router.post("/gerarEnconding", status_code=201, tags=["Generate encoding"])
async def person_encoding_router(file1, file2):
    return generate_enconding_handler(file1, file2)
