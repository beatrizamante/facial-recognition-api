import time
from app.controllers.face_controller import FaceController
from app.services.camera_feed import CameraFeed

if __name__ == "__main__":
    BACKEND_URL = "http://your-backend-url/authenticate"
    face_controller = FaceController()
    camera_feed = CameraFeed() 

    try:
        camera_feed.get_frame()
    except KeyboardInterrupt:
        print("Stopping the facial recognition API...")
    except Exception as e:
        print("An error occured: ", e)

