# from ...db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Date, Text
from app.api.models.user import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    starting_balance = Column(Float, nullable=False)
    latest_balance = Column(Float, nullable=False)
    name = Column(String(50), nullable=False)
    type = Column(String(20), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))


