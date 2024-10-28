from pathlib import Path

class UserModel:
    def __init__(self, db_path="data/user_encondings.pkl"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True, parents=True)
        self.db = self._load_database()
        
    def _load_database(self):
        if self.db_path.exists():
            with open(self.db_path, "rb") as f:
                return cryptography.load(f)
        return {}
    
    def save_database(self):
        with open(self.db_path, "wb") as f:
            crytography.dump(self.db, f)
            
    def add_user_enconding(self, user_id, encoding):
        self.db[user_id] = encoding
        self.save_database();
        
    

    
