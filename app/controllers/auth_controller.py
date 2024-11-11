from app.models.face_model import FaceModel
from app.models.db_connection import DbConnection

class FaceControllerJson:
    '''Classe responsável pelo service de reconhecimento'''
    def __init__(self):
        self.face_model = FaceModel()
        self.face_db = DbConnection()
        self.encoded_faces = []
        
    async def initialize(self):
        '''Essa função carrega todas as labels e encodings do banco'''
        self.encoded_faces = await self.load_database()
        
    async def load_database(self):
        '''Essa função é responsável por dar load nas encodings guardadas no banco'''
        database_results = await self.face_db.retrieve_encoded_faces()
        
        return database_results
    
    async def compare_with_db(self, new_encoding):
            '''Função para comparar o encoding do usuário atual com uma lista de encodings
            puxada da base de dados. Recebe como parâmetro o novo encoding e retorna o label do 
            usuário e true se houver match. Caso não, retorna o label vazio e um false boolean.'''
            #blob_to_numpy = self.face_model.blob_to_numpay_array(self.encoded_faces)
            label, is_match = self.face_model.calculate_face_distance(new_encoding, self.encoded_faces, threshold=0.5)
            if is_match:
                return label, True
            else:
                return "Desconhecido", False
                    

        
        