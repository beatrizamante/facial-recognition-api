from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import logging
from app.services.websocket_frame_process import app

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("uvicorn")

# app.mount("/static", StaticFiles(directory="static"), name="static")

# @app.get("/")
# async def get_index():
#     """Redirect to index.html in the static folder. THIS IS FOR TESTING ONLY"""
#     return RedirectResponse(url="/app/static/index.html")

if __name__ == "__main__":
    config = uvicorn.Config("main:app", 
                            host="172.16.21.53", 
                            port=443, 
                            ssl_certfile="./cert",
                            ssl_keyfile="./key"
                            )
    server = uvicorn.Server(config)
    server.run()
    


