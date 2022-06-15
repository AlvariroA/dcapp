from sqlalchemy import Column, Integer, String
from .database import Base 


class User(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    name = Column(String, index=True)
    email = Column(String, index=True, unique=True, nullable=False)
    

class Reciclaje(Base):
    __tablename__ = "reciclaje"
    
    id = Column(String, primary_key=True, index=True)
    usuario = Column(String, nullable=False)
    cantidad = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    puntos = Column(Integer, nullable=False)