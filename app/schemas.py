from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    edad: str
    telefono:str
    documento:str
    fecha_nac:str
    email:str
    hashed_password:str

class User(UserBase):
    id: str

    class Config:
        orm_mode = True

class UserUpdate(UserBase):
    pass

        
class Respuesta(BaseModel):
    mensaje:str
    
    
    
    
    
    
###Registro Prueba###
class ReciclajeBase(BaseModel):
    usuario: str
    cantidad: int
    tipo: str
    puntos: int
    imagen: str
           
class Reciclaje(ReciclajeBase):
    id: str

    class Config:
        orm_mode = True

class ReciclajeCreate(ReciclajeBase):
    pass

#######################