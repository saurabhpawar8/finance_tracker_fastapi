from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from dotenv import load_dotenv
import os

load_dotenv()

user = os.environ.get("DB_USER")
password = os.environ.get("DB_PASSWORD")
host = os.environ.get("DB_HOST")
db_name = os.environ.get("DB_NAME")

# Define the database connection UR
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{user}:{password}@{host}/{db_name}"

# Create a SQLAlchemy Engine object using the database URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory named SessionLocal for creating database sessions
# with specific configurations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create a base class for declarative class definitions
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
