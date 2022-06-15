from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id:Optional[int]
    name:str
    email:str
    
    class Config:
        orm_mode = True
        
class UserUpdate(BaseModel):
    name:str
    
    class Config:
        orm_mode = True
        
class Respuesta(BaseModel):
    mensaje:str
    
    
###Registro Prueba###
class ReciclajeBase(BaseModel):
    usuario: str
    cantidad: str
    tipo: str
    puntos: int
           
class Reciclaje(ReciclajeBase):
    id: str

    class Config:
        orm_mode = True

class ReciclajeCreate(ReciclajeBase):
    pass

#######################