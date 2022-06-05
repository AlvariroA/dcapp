from typing import Optional
from pydantic import BaseModel, Field, SecretStr, EmailStr
from enum import Enum
import os
import json

###Models
class TipoDocumento(str, Enum):
    cc: str="Cedula"
    pa: str='Pasaporte'
    ti: str='Tarjeta de Identidad'

class NombreLocalidad(Enum): 
    chapi="Chapinero"
    kenn="Kennedy"
    tunal="Tunal"

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


 
 