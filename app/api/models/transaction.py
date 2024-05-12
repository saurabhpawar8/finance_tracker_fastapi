# from ...db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Date, Text
from app.api.models.user import Base
from app.api.models.account import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    transaction_type = Column(String(20), nullable=False)
    date = Column(Date, nullable=False)
    remarks = Column(Text(50))
    user_id = Column(Integer, ForeignKey("users.id"))
    account_id = Column(Integer, ForeignKey("accounts.id"))
