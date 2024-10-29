import time
import threading
from app.controllers.face_recognition_service import FaceController

def display_camera_feed(face_controller):
    '''Function to display the camera feed in a separate thread.'''
    face_controller.view.display_feed()

if __name__ == "__main__":
    BACKEND_URL = "http://your-backend-url/authenticate"
    face_controller = FaceController()

    camera_thread = threading.Thread(target=display_camera_feed, args=(face_controller,))
    camera_thread.start()

    try:
        while True:
            response = face_controller.authenticate_user(BACKEND_URL)
            print("Response from backend:", response)
            time.sleep(10)  
    except KeyboardInterrupt:
        print("Stopping the facial recognition API...")

    camera_thread.join()
