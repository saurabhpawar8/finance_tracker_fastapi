from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette import status
from app.db.database import db_dependency
from app.api.models.account import Account

from app.api.services.user import user_dependecy

router = APIRouter()


class AccountRequest(BaseModel):
    starting_balance: float
    latest_balance: float
    name: str
    type: str


@router.post("/account")
async def createAccount(
    user: user_dependecy, db: db_dependency, accountRequest: AccountRequest
):
    account = Account(**accountRequest.model_dump(), user_id=user.get("user_id"))
    db.add(account)
    db.commit()
    return JSONResponse({"message": "Account created successfully"})
