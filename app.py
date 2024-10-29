import time
from app.controllers.face_recognition_service import FaceController

BACKEND_URL = "http://your-backend-url/endpoint"

if __name__ == "__main__":
    face_controller = FaceController()

    try:
        while True:
            response = face_controller.capture_and_send(BACKEND_URL)
            print("Response from backend:", response)
            time.sleep(30)
    except KeyboardInterrupt:
        print("Stopping the facial recognition API...")
