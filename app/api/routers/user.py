from typing import Annotated
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from app.api.models.user import User
from app.db.database import db_dependency
from app.api.services.user import bcrypt_context, authenticateUser, createAccessToken

router = APIRouter(prefix="/auth", tags=["auth"])


class CreateUserRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/", status_code=status.HTTP_201_CREATED)
async def createUser(db: db_dependency, userRequest: CreateUserRequest):
    userModel = User(
        email=userRequest.email,
        username=userRequest.email.split("@")[0],
        passowrd=bcrypt_context.hash(userRequest.password),
    )
    db.add(userModel)
    db.commit()


@router.post("/token", response_model=Token)
async def login_authentication(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticateUser(form_data.username, form_data.password, db)
    if not user:
        return JSONResponse({"Error": "Not Authenticated"})
    token = createAccessToken(user.username, user.id, timedelta(minutes=20))
    return JSONResponse({"access_token": token, "token_type": "bearer"})
