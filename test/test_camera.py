import cv2

def test_camera():
    while True:
        video_capture = cv2.VideoCapture(0)

        if not video_capture.isOpened():
            print("Could not open camera")
            return

        ret, frame = video_capture.read()
        if not ret:
            print("Could not read from camera")
        else:
            cv2.imshow("Camera Test", frame)
            cv2.waitKey(0)

        video_capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    test_camera()
