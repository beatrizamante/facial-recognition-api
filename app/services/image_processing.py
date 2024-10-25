from ...app.utils.helpers import resizing, 
import face_recognition
import cv2
import numpy as np 

video_capture = cv2.VideoCapture(0)

user_image = face_recognition.load_image_file("getUserImage")
user_face_encoding = face_recognition.face_encoding(user_image)[0]


known_face_encodings = [
    user_face_encoding,
]

known_face_names = [
    user_image,
]

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    ret, frame = video_capture.read()
    resizing(frame);
    
    if process_this_frame:
        
        rgb_small_frame = frame[:, :, ::-1]
        
    face_locations = face_recognition.face_locations(rgb_small_frame);
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations);
    
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