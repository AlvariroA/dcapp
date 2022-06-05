# Python
from typing import Optional, List, Dict

# Pydantic
from pydantic import BaseModel, Field

#starlette
from starlette.responses import HTMLResponse

# FastAPI
from fastapi import FastAPI
from fastapi import Query, Path, HTTPException, status, Body, Request, Response, Form
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse


from database import reciclajes

templates = Jinja2Templates(directory="templates")

class Reciclaje(BaseModel):
    usuario: Optional[str]
    cantidad: Optional[str]
    tipo: Optional [str] 
    puntos: Optional[float]

     
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

##########################################
    
####Pagina Inicio    
@app.get("/", response_class=RedirectResponse)
async def root(request: Request):
    return RedirectResponse(url="/reciclajes")


####Listar Reciclajes
@app.get(path="/reciclajes",
         response_class=HTMLResponse,
         #response_model=List[Dict[str, Car]],
         tags=["Get"],
         summary="List all cars",
         status_code=status.HTTP_200_OK
         )
def get_reciclajes(request: Request, number: Optional[str] = Query("10", max_length=3)):
    response = []
    for id, reciclaje in list(reciclajes.items())[:int(number)]:
        response.append((id, reciclaje))
    return templates.TemplateResponse("index.html", {"request":request, "reciclajes":response, "title":"Reciclajes"})



@app.post("/search", response_class=RedirectResponse)
def search_reciclaje(id: str = Form(...)):
    return RedirectResponse("/reciclajes/" + id, status_code=status.HTTP_302_FOUND)
    
    
####Consular por id
@app.get(path="/reciclajes/{id}",
         response_class=HTMLResponse,
         status_code=status.HTTP_200_OK,
         tags=["Reciclaje"],
         summary="Find car by Id")
def get_car_by_id(request: Request, id: int = Path(..., ge=0, lt=1000)):
    reciclaje = reciclajes.get(id)
    response = templates.TemplateResponse("search.html", {"request": request, "reciclaje": reciclaje, "id":id, "title": "Reciclaje"})
    if not reciclaje:
        response.status_code=status.HTTP_404_NOT_FOUND
    return response

####Registro de un nuevo reciclaje
@app.get("/create", response_class=HTMLResponse)
def create_registro(request:Request):
    return templates.TemplateResponse("create.html", {"request":request, "title": "Create Reciclaje"})



@app.post(path="/reciclajes",
          status_code=status.HTTP_201_CREATED,
          tags=["Cars"],
          summary="Add a car")
def add_registro(
    usuario: Optional[str] = Form(...),
    cantidad: Optional[str] = Form(...),
    tipo: Optional [str] = Form(...),
    puntos: Optional[float] = Form(...),
    min_id: Optional[int]= Body(0)):
    body_reciclajes= [Reciclaje(usuario=usuario, cantidad=cantidad, tipo=tipo, puntos=puntos)]
    if len(body_reciclajes) < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No cars to add")
    min_id = len(reciclajes.values())+min_id
    for reciclaje in body_reciclajes:
        while reciclajes.get(min_id):
            min_id+=1
        reciclajes[min_id]=reciclaje
        min_id+=1
    return RedirectResponse(url="/reciclajes", status_code=status.HTTP_302_FOUND)
