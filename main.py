from typing import Optional
from pydantic import BaseModel, Field, SecretStr, EmailStr
from enum import Enum
import os

from fastapi import FastAPI
from fastapi import Body, Query, Path
from fastapi import status
from fastapi import Form, Cookie, Header
from fastapi import File, UploadFile

from fastapi.responses import FileResponse 
from fastapi import HTTPException

app = FastAPI()


#Utilities


###Enumaraciones
class TipoDocumento(Enum):
    cc="Cedula"
    pa="Pasaporte"
    ti="Tarjeta de Identidad"

class NombreLocalidad(Enum):
    chapi="Chapinero"
    kenn="Kennedy"
    tunal="Tunal"
    
    


def directory_is_ready():
    os.makedirs(os.getcwd()+"/img",exist_ok=True) 
    return os.getcwd()+"/img/"


###Models


class PersonBase(BaseModel):
    fist_name: str=Field(
        ...,
        min_length=2,
        max_length=50,
        example="Alvaro" 
    )
    last_name: str=Field(
        ...,
        min_length=2,
        max_length=50,
        example="Avila"
    )
    age: int=Field(
        ...,
        gt=0,
        le=100,
        example=22
    )
    email: EmailStr=Field(
        ...,
        example="alvarin@ucatolica.com"
    )
    tipo_documento: TipoDocumento=Field(
        default = None,
        example = TipoDocumento.cc
    )
    documento: str=Field(
        ...,
        min_length=8,
        example = "xxxxxxxxx"
    )
    telefono:str=Field(...)


class Administrador(PersonBase):
    codigo_administador: int=Field(
        ...,
        gt=0,
        example="001")
    emailDcapp: EmailStr=Field(
        ...,
        example="admin@dcapp.com"
    )
    
class Usuario(PersonBase):
    codigo_usuario: int=Field(
        ...,
        gt=0,
        example="U-001")
    
    puntos:int=Field(
        ...,
        gt=0,
        example="100"
    )
    estado_app:bool=Field(default=False)
    
class Sponsor(PersonBase):
    codigo_sponsor: int=Field(
        ...,
        gt=0,
        example="001")
    fecha_vencimiento: str=Field(
        ...,
        example="22/04/2022"
    )
    
class LoginOut(BaseModel):
    username: str=Form(
        ...,
        min_length=3,
        max_length=20,
        example="adavila59"
    )
    password: SecretStr=Form(
        ...,
        min_length=6,
    )
    message : str=Field(
        default="Success"
    )        
    
@app.get("/",status_code=status.HTTP_200_OK,tags=["Mensaje"],
          summary="Logeo de un usuario")
def home():
    return {"Bienvenido":"DCAPP"}


######Metodos######

#Crear nuevo usuario
@app.post(path="/registro/new",
          status_code=status.HTTP_201_CREATED,
          tags=["Users"],
          summary="Logeo de un usuario")
def new_person(person:Usuario=Body(...)):
    return person



#Login
@app.post(path="/login", 
          status_code=status.HTTP_200_OK, 
          response_model=LoginOut,
          tags=["Users"],
          summary="Logeo de un usuario")
def Login(
#Inicio de Secion
    username:str = Form(...),
    password:str = Form(...)
):
    return LoginOut(username=username, password=password)


#Help

##USUARIOS

#ver usuario

#ver meta

#ver lugar de reciclaje

#ver reciclaje

#puntos 





##ADMINISTRADOR##

#ver Administrador

#listar USUARIOS

#listar ecopuntos

#info ecopunto

#agregar nuevo ecopunto

#listar mensajes