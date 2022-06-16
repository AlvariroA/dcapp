from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base 
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    name = Column(String, index=True)
    email = Column(String, index=True, unique=True, nullable=False)
    

class Reciclaje(Base):
    __tablename__ = "reciclaje"
    
    id = Column(String, primary_key=True, index=True)
    usuario = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
    puntos = Column(Integer, nullable=False)
    imagen = Column(String)