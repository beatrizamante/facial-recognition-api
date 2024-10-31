import face_recognition
import json
import os

def encode_images_with_labels(images_path):
    encodings = []
    for image_file in os.listdir(images_path):
        
        label = image_file.split('-')[0]
        print("Label:", label)
        
        image_path = os.path.join(images_path, image_file)
        
        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image)
        encoding = face_recognition.face_encodings(image, face_locations)
        print("Encoding:", encoding)

        if encoding:
            encodings.append({"label": label, "encoding": encoding[0].tolist()})
        else:
            print(f"No face detected in {image_file}")
    
    with open("encoded_faces.json", "w") as f:
        json.dump(encodings, f)
    
    print("Encodings saved successfully.")

encode_images_with_labels("/test_images")
