import os

from fastapi import APIRouter
from fastapi import FastAPI
from fastapi import Response, Request, Depends, status, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder


#starlette
from starlette.responses import HTMLResponse
from starlette.responses import RedirectResponse

##DataBase
import app.models as models
import app.schemas as schemas
import app.database as db
import app.crud as crud
from app.database import engine
from typing import List 

from sqlalchemy.orm import Session

###TOKEN
from dotenv import load_dotenv
from routes.auth import auth_routes
from passlib.context import CryptContext

###routes
from routes.dcapp_users import dcapp_users
from routes.auth import auth_routes

pwd_ctx= CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()
users = APIRouter()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/img", StaticFiles(directory="img"), name="img")


app.include_router(auth_routes, prefix="/api")
app.include_router(dcapp_users, prefix ="/api")
load_dotenv()

def get_hashed_password(plain_password):
    return pwd_ctx.hash(plain_password)

def verify_password(plain_password, hashed_password):
    return pwd_ctx.verify(plain_password, hashed_password)




def directory_is_ready():
    os.makedirs(os.getcwd()+"/img", exist_ok=True)
    return os.getcwd()+"/img/"



###Conexion con la base de datos

        
"""@dcapp_users.post("/home")
def root(request: Request):
    return templates.TemplateResponse("usuario/home.html", {"request": request, "title": "Home"})"""



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



@app.post("/signin")
def register(request: Request,
             username:str=Form(...),
             edad:str=Form(...),
             telefono:str=Form(...),
             email:str=Form(...),
             documento:str=Form(...),
             fecha_nac:str=Form(...),
             password:str=Form(...),
             db: Session=Depends(db.get_db)):
    hashed_password=get_hashed_password(password)
    invalid=False

    if crud.get_user_by_username(db=db, username=username):
        invalid = True
    if crud.get_user_by_email(db=db, email=email):
        invalid = True
    if not invalid:
        crud.create_user(db=db, user=schemas.UserUpdate(
            username=username,
            edad=edad,
            telefono=telefono,
            email=email,
            documento=documento,
            fecha_nac=fecha_nac,
            hashed_password=hashed_password
        ))
        resposnse = RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
        return resposnse
    else:
        return templates.TemplateResponse("signin.html",
                                          {"request":request,
                                           "title":"Register",
                                           "invalid": invalid},
                                          status_code=status.HTTP_400_BAD_REQUEST)

















####Reciclaje
@app.get("/reciclaje")
def get_register(request: Request):
    return templates.TemplateResponse("create.html",{"request":request, "title": "Registro"})


@app.get("/create", response_class=HTMLResponse)
def create_registro(request:Request):
    return templates.TemplateResponse("create.html", {"request":request, "title": "Create Reciclaje"})

@app.post("/reciclaje")
async def register(request: Request,
             usuario:str=Form(...),
             cantidad:int=Form(...),
             tipo:str=Form(...),
             imagen: UploadFile = File(...),
             db: Session=Depends(db.get_db)):
    dir = directory_is_ready()
    print(dir)
    with open(dir+imagen.filename, "wb") as myimage:
        content = await imagen.read()
        myimage.write(content)
        myimage.close()
    puntos = 100
    crud.create_reciclaje(db=db, reciclaje=schemas.ReciclajeCreate(
        usuario=usuario,
        cantidad=cantidad,
        tipo=tipo,
        puntos = puntos,
        imagen=imagen.filename
    ))
    responseReciclaje = RedirectResponse("/reciclaje", status_code=status.HTTP_302_FOUND)
    return responseReciclaje


@app.get(path="/reciclajes",
         response_class=HTMLResponse,
         response_model=schemas.Reciclaje,
         tags=["Get"],
         summary="List all cars",
         status_code=status.HTTP_200_OK
         )
def get_reciclajes(request: Request, db: Session = Depends(db.get_db)):
    result = db.query(models.Reciclaje).all()
    result2 = jsonable_encoder(result)
    response = []
    for reciclaje in result2:
        response.append((reciclaje))
    return templates.TemplateResponse("index.html",
                                      {"request": request, "reciclajes": response, "title": "Lista Reciclajes"})

####### Usuarios 



@app.get("/users")
def get_users(db:Session=Depends(db.get_db), user:schemas.User=Depends(db.get_db)):
    result=crud.get_users(db=db)
    return jsonable_encoder(result)

models.Base.metadata.create_all(engine)
    





    