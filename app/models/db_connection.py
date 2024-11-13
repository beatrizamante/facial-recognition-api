import psycopg2
from dotenv import load_dotenv
import os
import pickle

load_dotenv()

class DbConnection:
    '''Função responsável por criar conexão com o banco de dados
    para retorno de informações.'''
    
    def __init__(self): 
        self.connection = psycopg2.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_DATABASE')
            )    
    
    async def retrieve_encoded_faces(self):
        '''Função responsável por retornar todos os encodes facias dos usuários
        que estão salvos no banco.'''
        
        encodings = []
        cur = self.connection.cursor()
        cur.execute('SELECT "nome", "email", "hash", "hash1" FROM operacional.conf_usuario')
        records = cur.fetchall()
        
        for record in records:
            label = record[0] 
            mail = record[1] 
            binary_hashes = [record[2], record[3]]
            encoding_list = []
            for binary_hash in binary_hashes:
                if binary_hash in binary_hashes:
                    try:
                        encoding = pickle.loads(binary_hash)  
                        encoding_list.append(encoding)
                    except (pickle.UnpicklingError, TypeError) as e:
                        print(f"Error decoding hash for {label}: {e}")
            if encoding_list:
                encodings.append({"label": label, "mail": mail, "encoding": encoding_list})      
        return encodings
    
            
         

        