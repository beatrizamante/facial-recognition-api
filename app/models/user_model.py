'''Modulo usado para extrair a informação do usuário do banco de dados e
comparar com a imagem da câmera'''

from pathlib import Path

class UserModel:
    '''Classe usada para fazer carregamento de enconding faciais dos usuários e salvar 
    novos dentro do mesmo caminho. Caso o diretório não exista, este cria um.'''
    
    def __init__(self, db_path="data/user_encondings.pkl"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True, parents=True)
        self.db = self._load_database()
        
    def _load_database(self):
        '''Função utilizada para carregar o diretório de encondings já criados no banco 
        'rb - read binary' caso esse diretório já exista.'''
        if self.db_path.exists():
            with open(self.db_path, "rb") as f:
                return cryptography.load(f)
        return {}
    
    def save_database(self):
        '''Função utilizada para salvar 'wb - write binary' o encoding facial do usuário dentro 
        de um caminho no banco de dados. Função sem retorno.'''
        with open(self.db_path, "wb") as f:
            crytography.dump(self.db, f)
            
    def add_user_enconding(self, user_id, encoding):
        '''Função para adicionar os encondings dentro do banco de dados. Recebe o id do usuário
        e o enconding referente ao mesmo e salva dentro da base de dados.'''
        self.db[user_id] = encoding
        self.save_database()
        
        