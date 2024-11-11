import os
from sqlalchemy import Column, DateTime, Integer, LargeBinary, String, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DB_URL")
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'conf_usuario'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100))
    departamento = Column(String(100))
    email=Column(String(100))
    ativo=Column(bool)
    dataCadastro=Column(DateTime, default=func.now())
    dataAlteracao=Column(DateTime, default=func.now(), onupdate=func.now())
    usuarioCadastro=Column(String(100))
    usuarioAlteracao=Column(String(100))
    hash = Column(LargeBinary)  

Base.metadata.create_all(bind=engine)
