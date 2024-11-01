from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from app.services.websocket_frame_process import app

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def get_index():
    """Redirect to index.html in the static folder."""
    return RedirectResponse(url="/static/index.html")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    

    # auth_service = FaceController()

    # try:
    #      auth_service.authenticate_user_clientside()
    # except KeyboardInterrupt:
    #     print("Stopping the facial recognition API...")
    # except Exception as e:
    #     print("An error occured: ", e)

