from cv2 import cv2
import face_recognition
import numpy as np
from app.utils.helpers import resizing

video_capture = cv2.VideoCapture(0)

user_image = face_recognition.load_image_file("getUserImage")
user_face_encoding = face_recognition.face_encodings(user_image)[0]

known_face_encodings = [
    user_face_encoding,
]

known_face_names = [
    user_image,
]

face_locations = []
face_encodings = []
face_names = []
PROCESS_THIS_FRAME = True

while True:
    ret, frame = video_capture.read()
    resizing(frame)
    if PROCESS_THIS_FRAME:
        rgb_small_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame);
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    face_names = [];
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "User unknown"
        #if True in matches:
        #    first_match_index = matches.index(True);
        #    name = known_face_names[first_match_index]
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]