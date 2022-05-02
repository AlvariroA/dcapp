from typing import Optional
from pydantic import BaseModel, Field, SecretStr, EmailStr
from enum import Enum
import os
import json

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
    
#Pruebas
ecopunto2 = {"id_ecopunto":"55", "direccion":"cra 45 B", "localidad":NombreLocalidad.chapi}
mensajes = {"1":"Hola Como Estas", "2":"Esta es una prueba"}
validarMeta = {"1":"Tu meta es la siguiente: 500 pts"}


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
class reciclaje(Usuario):
    name_reciclaje: str=Field(
        ...,
        min_length=3,
        max_length=20
    )
    cantidad_r: int=Field(
        ...,
        gt=0,
        example="001"
    )
    codigo_recicla: int=Field(
        ...,
        gt=0,
        example="001"
    )
class puntos(Usuario):
    cantidad_puntos: int=Field(
        ...,
        gt=0,
        example="001"
    )


    
    
    
    
    
    
    
@app.get("/",status_code=status.HTTP_200_OK,
         tags=["Inicio"],
         summary="Inicio pagina DCAPP")
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
#Enviar datos
    username:str = Form(...),
    password:str = Form(...)
):
    return LoginOut(username=username, password=password)


#Help

##USUARIOS

#ver usuario
@app.get('/{cod_usuario}/',
         tags=["Users"],
         summary="Inicio usuario")
def get_post(cod_usuario: int):
    for post in post:
            if post["codigo_usuario"]== cod_usuario:
                return post
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Persona no registrada")


#ver meta
@app.get("/{nombreusuario}/meta",status_code=status.HTTP_200_OK,
         tags=["Users"],
         summary="Presenta la meta de reciclaje de cada usuario")
def meta(
    nombreusuario:str=Path(...)
):
    return validarMeta


#ver lugar de reciclaje
@app.get("/{nombreusuario}/lugarReciclaje/{codigo_lugar}",tags=["Users"],
         summary="Presenta el lugar de reciclaje de cada usuario")
def get_post(cod_lugar: int):
    for post in post:
            if post["codigo_lugar"] == cod_lugar:
                return post
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Punto no encontrado")


#ver reciclaje
@app.get(
    path="/reciclaje/{cod_reciclaje}",
    status_code=status.HTTP_404_NOT_FOUND,tags=["Users"],
         summary="Presenta reciclaje de cada usuario")
def home():
    return  reciclaje




#puntos
@app.get(
    path="/{nombreusuario}/reciclaje/puntos",
    status_code=status.HTTP_404_NOT_FOUND,tags=["Users"],
         summary="Presenta los puntos de cada usuario"
)
def home():
    return  puntos

#Crear registro reciclaje
@app.post(path="/{nombreusuario}/reciclaje/new",
          status_code=status.HTTP_201_CREATED,
          tags=["Users"],
          summary="Registro de reciclaje")
def new_reciclaje(reci:reciclaje=Body(...)):
    return reci



##ADMINISTRADOR##

#ver Administrador
@app.get('/post/{cod_admi}',
         tags=["Admin"],
         summary="Muestra perfil de administrador")
def get_post(cod_admi: int):
    for post in post:
            if post["codigo_administador"]== cod_admi:
                return post
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="administrador no registrada")
#listar USUARIOS

@app.get(
    path="/{nombreadministrador}/usuarios",
    status_code=status.HTTP_200_OK,
    tags=["Admin"],
    summary="Listar todos los usuarios"
)
def list_all_users():
    with open("users.json","r+",encoding="utf-8") as file:
        current=json.loads(file.read())
    return current


#listar ecopuntos
@app.get(
    path="/{codigo_administrador}/reciclaje",
    status_code=status.HTTP_200_OK,
    tags=["Admin"],
    summary="Listar todos los reciclajes"
)
def list_all_reciclaje():
    """
    with open("reciclaje.json","r+",encoding="utf-8") as file:
        current=json.reciclaje(file.read())
    return current
    """
    def listar_reciclaje(
    codigo_administrador:str = Path(...)
):
        return mensajes


#info ecopunto
@app.get("/{codigo_administador}/ecopuntos/{codigo_ecopunto}",
         status_code=status.HTTP_200_OK,
         tags=["Admin"],
         summary="Presenta la información de un ecopunto")
def info_ecopunto(
    codigo_administador:str = Path(...),
    codigo_ecopunto:str = Path(...)
):
    return ecopunto2

#agregar nuevo ecopunto
@app.post(path="/{codigo_administador}/ecopuntos/new",
          status_code=status.HTTP_201_CREATED,
          tags=["Ecopunto"],
          summary="Registro de un nuevo ecopunto")
def new_ecopunto(
    codigo_administador: str=Path(...),
    
    id_ecopunto: str=Form(
        ...,
    ),
    nombre_ecopunto: str=Form(...),
    localidad: NombreLocalidad=Form(...)
):
    return ecopunto2

#listar mensajes -tmb

@app.get("/{codigo_administador}/buzon/",
         status_code=status.HTTP_200_OK,
         tags=["Admin"],
         summary="Aqui se listan los mensajes de los usuario")
def listar_mensajes(
    codigo_administador:str = Path(...)
):
    return mensajes