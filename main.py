from app.controllers.face_controller import FaceController
from app.services.camera_feed import CameraFeed

if __name__ == "__main__":
    BACKEND_URL = "http://your-backend-url/authenticate"
    auth_service = FaceController()

    try:
        auth_service.authenticate_user(backend_url=BACKEND_URL)
    except KeyboardInterrupt:
        print("Stopping the facial recognition API...")
    except Exception as e:
        print("An error occured: ", e)

