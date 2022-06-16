from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse


import app.schemas as schemas
from app.functions_jwt import write_token, validate_token



auth_routes = APIRouter()


@auth_routes.post("/login")
def login(user: schemas.User):
    print(user.dict())
    if user.name == "Alvaro Avila":
        return write_token(user.dict())
    return JSONResponse(content = {"message": "User not found"}, status_code = 404)

@auth_routes.post("/verify/token")
def verify_token(Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    return validate_token(token, output=True)