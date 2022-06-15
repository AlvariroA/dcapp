from sqlalchemy.orm import Session
from . import models, schemas
import uuid


def get_users(db:Session):
    return db.query(models.User).filter(models.User.id==id).first()

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
        puntos=int(reciclaje.puntos)
    )
    db.add(db_reciclaje)
    db.commit()
    db.refresh(db_reciclaje)

    return db_reciclaje
############################################