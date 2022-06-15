from fastapi import FastAPI
from fastapi import Response, Request, Depends, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder


#starlette
from starlette.responses import HTMLResponse
from starlette.responses import RedirectResponse


from . import models, schemas, crud

from . import database as db
from .database import SessionLocal, engine

from typing import List 

from sqlalchemy.orm import Session



models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

###Conexuion con la base de datos

        




####Crud Basico
@app.get('/usuarios/',response_model=List[schemas.User])
def show_users(db:Session=Depends(db.get_db)):
    usuarios = db.query(models.User).all()
    return usuarios

@app.post('/usuarios/',response_model=schemas.User)
def create_users(entrada:schemas.User, db:Session=Depends(db.get_db)):
    usuario = models.User(id = int(entrada.id), name = entrada.name, email = entrada.email)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

@app.put('/usuarios/{usuario_id}',response_model=schemas.User)
def create_users(usuario_id:int, entrada:schemas.UserUpdate, db:Session=Depends(db.get_db)):
    usuario = db.query(models.User).filter_by(id=usuario_id).first()
    usuario.name=entrada.name
    db.commit()
    db.refresh(usuario)
    return usuario

@app.delete('/usuarios/{usuario_id}',response_model=schemas.Respuesta)
def delete_users(usuario_id:int,db:Session=Depends(db.get_db)):
    usuario = db.query(models.User).filter_by(id=usuario_id).first()
    db.delete(usuario)
    db.commit()
    respuesta = schemas.Respuesta(mensaje = "Eliminado exitosamente")
    return respuesta


####Response in HTMLResponse

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("inicio/index.html", {"request": request, "title": "Home"})


@app.get("/signin")
def root(request: Request):
    return templates.TemplateResponse("inicio/signin.html", {"request": request, "title": "Home"})

@app.get("/login")
def root(request: Request):
    return templates.TemplateResponse("inicio/login.html", {"request": request, "title": "Home"})


####Autentificación







@app.get("/users")
def get_users(db:Session=Depends(db.get_db), user:schemas.User=Depends(db.get_db)):
    result=crud.get_users(db=db)
    return jsonable_encoder(result)


@app.get("/register")
def get_register(request: Request):
    return templates.TemplateResponse("create.html",{"request":request,
                                                        "title": "Registro"})
    



@app.get("/reciclajes")
def get_reciclajes(db:Session=Depends(db.get_db)):
    result=crud.get_reciclajes(db=db)
    return jsonable_encoder(result)

@app.get("/create", response_class=HTMLResponse)
def create_registro(request:Request):
    return templates.TemplateResponse("create.html", {"request":request, "title": "Create Reciclaje"})

@app.post("/reciclajes")
def register(request: Request,
             usuario:str=Form(...),
             cantidad:str=Form(...),
             tipo:str=Form(...),
             puntos:int=Form(...),
             db: Session=Depends(db.get_db)):
    crud.create_reciclaje(db=db, reciclaje=schemas.ReciclajeCreate(
        usuario=usuario,
        cantidad=cantidad,
        tipo=tipo,
        puntos=puntos
    ))
    responseReciclaje = RedirectResponse("/reciclajes", status_code=status.HTTP_302_FOUND)
    return responseReciclaje

    