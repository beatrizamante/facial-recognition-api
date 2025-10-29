import psycopg2
class DbConnection:
    '''Função responsável por criar conexão com o banco de dados
    para retorno de informações.'''

    def __init__(self):
        self.settings = Settings()
        self.connection = psycopg2.connect(
            user=self.settings.DB_USER,
            password=self.settings.DB_PASSWORD,
            host=self.settings.DB_HOST,
            port=self.settings.DB_PORT,
            database=self.settings.DB_DATABASE
            )
