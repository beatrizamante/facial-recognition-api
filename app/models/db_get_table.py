import os
from sqlalchemy import Boolean, Column, DateTime, Integer, LargeBinary, String, create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DB_URL')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'conf_usuario'
    __table_args__ = {'schema': 'operacional'}

    idUsuario = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    departamento = Column(String(100))
    matricula = Column(String, nullable=False)
    email=Column(String(100), nullable=False, unique=True)
    ativo=Column(Boolean, default=True)
    dataCadastro=Column(DateTime)
    dataAlteracao=Column(DateTime)
    usuarioCadastro=Column(String(100))
    usuarioAlteracao=Column(String(100))
    hash = Column(LargeBinary)  

Base.metadata.create_all(bind=engine)
