
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Date, Text
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    email = Column(String(50), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    passowrd = Column(String(100), nullable=False)
