
import base64
import pickle


def encode_to_base64(data):
    """Codifica os dados binários para Base64 para armazenar em JSON"""
    return base64.b64encode(pickle.dumps(data)).decode('utf-8')