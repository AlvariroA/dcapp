from sqlalchemy.orm import Session
from . import models, schemas
import uuid


def get_users(db:Session, id:str):
    return db.query(models.User).filter(models.User.id==id).first()


def get_user_by_username(db:Session, username: str):
    return db.query(models.User).filter(models.User.username==username).first()

def get_user_by_email(db:Session, email:str):
    return db.query(models.User).filter(models.User.email==email).first()






def get_reciclajes(db:Session):
    return db.query(models.Reciclaje).all()

def get_reciclaje(db: Session, id:str):
    return db.query(models.Reciclaje).filter(models.Reciclaje.id==id).first()


###########################################
def create_reciclaje(db:Session, reciclaje: schemas.ReciclajeCreate):
    id = uuid.uuid4()
    while get_reciclaje(db=db, id=str(id)):
        id = uuid.uuid4()
    db_reciclaje=models.Reciclaje(
        id=str(id),
        usuario=reciclaje.usuario,
        cantidad=reciclaje.cantidad,
        tipo=reciclaje.tipo,
        puntos=reciclaje.puntos,
        imagen=reciclaje.imagen
    )
    db.add(db_reciclaje)
    db.commit()
    db.refresh(db_reciclaje)

    return db_reciclaje
############################################
def create_user(db:Session, user: schemas.UserUpdate):
    id = uuid.uuid4()
    while get_users(db=db, id=str(id)):
        id = uuid.uuid4()
    db_user=models.User(
        id=str(id),
        username=user.username,
        edad=user.edad,
        telefono=user.telefono,
        email=user.email,
        hashed_password=user.hashed_password,
        fecha_nac=user.fecha_nac,
        documento=user.documento
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
