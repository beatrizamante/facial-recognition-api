import json
import numpy as np
from face_recognition import face_distance

def load_mock_db(filename):
    with open(filename, "r") as f:
        return json.load(f)

def compare_encodings(known_encodings, real_time_encoding, tolerance=0.6):
    for entry in known_encodings:
        label = entry["label"]
        known_encoding = np.array(entry["encoding"])
        distance = face_distance([known_encoding], real_time_encoding)[0]
        if distance <= tolerance:
            print(f"Match found for {label} with distance {distance}")
            return label
    print("No match found")
    return None

# Load the mock database
mock_db = load_mock_db("mock_db.json")

# Example real-time encoding to compare
real_time_encoding = [/* insert real-time encoding array here */]

# Compare
result = compare_encodings(mock_db, real_time_encoding)
