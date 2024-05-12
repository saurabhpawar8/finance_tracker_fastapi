from typing import Annotated
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from app.api.models.user import User

SECRET_KEY = "y9833943gbg37i9321bsxx12e"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def authenticateUser(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.passowrd):
        return False
    return user


def createAccessToken(username: str, userId: int, expiresDelta: timedelta):
    encode = {"sub": username, "id": userId}
    expires = datetime.now() + expiresDelta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def getCurrentUser(token: Annotated[str, Depends(oauth_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")

        if username is None and user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return {"username": username, "user_id": user_id}
    except JWTError:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="COuld not validate user"
        )


user_dependecy = Annotated[dict, Depends(getCurrentUser)]
