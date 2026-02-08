from pathlib import Path
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, create_engine, SQLModel

# get the database url
DATABASE_URL = Path(__file__).resolve().parent.parent.parent/"database.db"

# connect args
connect_args = {"check_same_thread": False}

# create the engine
engine = create_engine(f"sqlite:///{DATABASE_URL}", connect_args=connect_args)


# get the session
def get_session():
    print(f"Database URL: {DATABASE_URL}")
    with Session(engine) as session:
        yield session


# session dependency
SessionDep = Annotated[Session, Depends(get_session)]


# create the database and tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
