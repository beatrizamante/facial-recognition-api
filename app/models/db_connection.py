import psycopg2
from dotenv import load_dotenv
import os
import ast

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
        cur.execute('SELECT pes."nomeClassificador", pes."hashclassificador" FROM app_classificacao_dev.pes_classificador as pes  WHERE pes."idClassificador" = 1')
        records = cur.fetchall()
        encodings = [{"label": record[0], "encoding": ast.literal_eval(record[1])} for record in records]
        return encodings

        