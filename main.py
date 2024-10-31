from app.controllers.face_controller_client import FaceController

if __name__ == "__main__":
    BACKEND_URL = "http://your-backend-url/authenticate"
    auth_service = FaceController()

    try:
        auth_service.authenticate_user_clientside()
    except KeyboardInterrupt:
        print("Stopping the facial recognition API...")
    except Exception as e:
        print("An error occured: ", e)

