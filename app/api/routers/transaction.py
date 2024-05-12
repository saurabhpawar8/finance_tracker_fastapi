from fastapi import APIRouter, Depends, HTTPException, Path, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from starlette import status
from app.db.database import db_dependency
from app.api.models.transaction import Transaction
from app.api.models.account import Account
from typing import Annotated
from app.api.services.account import getAccountIDByAnme
from datetime import datetime
from app.api.services.user import user_dependecy
from sqlalchemy import and_

router = APIRouter()


class TransacationRequest(BaseModel):
    amount: int
    category: str
    transaction_type: str
    date: str
    remarks: str
    account: str


class AllTransactionsRequest(BaseModel):
    category: str
    transaction_type: str
    from_date: str
    to_date: str
    account: str


@router.post("/transaction")
async def createTransaction(
    user: user_dependecy, db: db_dependency, transactionRequest: TransacationRequest
):
    account = getAccountIDByAnme(transactionRequest.account, db)
    print(account)
    transaction = Transaction(
        amount=transactionRequest.amount,
        category=transactionRequest.category,
        transaction_type=transactionRequest.transaction_type,
        date=datetime.strptime(transactionRequest.date, "%Y-%m-%d").date(),
        remarks=transactionRequest.remarks,
        account_id=account,
        user_id=user.get("user_id"),
    )

    db.add(transaction)
    db.commit()
    return JSONResponse({"message": "Transaction created successfully"})


@router.post("/get_all_transactions")
async def getAllTransactions(
    user: user_dependecy,
    db: db_dependency,
    allTransactionRequest: AllTransactionsRequest,
):

    # if allTransactionRequest.category != "ALL":
    #     transactions = (
    #         db.query(Transaction.amount, Account.name)
    #         .join(Account, Transaction.account_id == Account.id)
    #         .filter(
    #             and_(
    #                 Transaction.date.between(
    #                     allTransactionRequest.from_date, allTransactionRequest.to_date
    #                 ),
    #                 category=Transaction.category,
    #             )
    #         )
    #         .all()
    #     )
    transactions = (
        db.query(Transaction.amount, Account.name)
        .join(Account, Transaction.account_id == Account.id)
        .filter(
            Transaction.date.between(
                allTransactionRequest.from_date, allTransactionRequest.to_date
            )
        )
        .all()
    )
    print(transactions)
    result_dicts = [row._asdict() for row in transactions]

    return result_dicts
