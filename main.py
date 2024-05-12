from fastapi import FastAPI
from app.db.database import engine, Base
from app.api.routers import transaction, user, account

app = FastAPI()

Base.metadata.create_all(bind=engine)


app.include_router(transaction.router)
app.include_router(user.router)
app.include_router(account.router)
