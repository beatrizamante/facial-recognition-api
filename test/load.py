import json

class LoadData:

    def load_encoded_faces(self, filepath):
            '''Load encoded faces from a JSON file.'''
            try:
                with open(filepath, "r") as f:
                    return json.load(f)
            except Exception as e:
                print("Error loading encoded faces:", e)
                return []