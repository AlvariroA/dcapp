from fastapi import APIRouter

from fastapi import Response, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from middlewares.verify_token_route import VerifyTokenRoute

dcapp_users = APIRouter(route_class=VerifyTokenRoute)
templates = Jinja2Templates(directory="templates")
dcapp_users.mount("/static", StaticFiles(directory="static"), name="static")
dcapp_users.mount("/img", StaticFiles(directory="img"), name="img")

@dcapp_users.get("/home")
def root(request: Request):
    return templates.TemplateResponse("usuario/home.html", {"request": request, "title": "Home"})