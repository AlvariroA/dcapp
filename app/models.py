from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base 
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    username = Column(String, index=True)
    edad = Column(String)
    telefono = Column(String, index=True, unique=True, nullable=False)
    documento = Column(String, index=True, unique=True, nullable=False)
    fecha_nac = Column(String, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    hashed_password = Column(String, index=True, unique=True, nullable=False)

class Reciclaje(Base):
    __tablename__ = "reciclaje"
    
    id = Column(String, primary_key=True, index=True)
    usuario = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
    puntos = Column(Integer, nullable=False)
    imagen = Column(String)