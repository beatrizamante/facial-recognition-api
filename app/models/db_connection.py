from hdbcli import dbapi
from dotenv import load_dotenv
import os
import json

load_dotenv()

class DbConnection:
    def __init__(self):
        self.connection = dbapi.connect(
            address=os.getenv('DB_ADDRESS'),
            port=os.getenv('DB_PORT'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )

    async def retrieve_encodings(self):
        '''Função para pegar os encodings do banco e retorná-los.'''
        encodings = []
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT user_id, encoding FROM Encodings")
            for user_id, encoding_blob in cursor.fetchall():
                encoding = json.loads(encoding_blob) 
                encodings.append({"user_id": user_id, "encoding": encoding})
            cursor.close()
        except Exception as e:
            print("Error retrieving encodings:", e)
        return encodings
