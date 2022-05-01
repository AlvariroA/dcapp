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
    
    
@app.get("/",status_code=status.HTTP_200_OK)
def home():
    return {"Bienvenido":"DCAPP"}