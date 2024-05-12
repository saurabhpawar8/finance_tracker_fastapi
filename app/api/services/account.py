from app.api.models.account import Account


def getAccountIDByAnme(account: str, db):
    account_id = db.query(Account.id).filter(Account.name == account).scalar()
    return account_id
