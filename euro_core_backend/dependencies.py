from sqlalchemy import create_engine
from sqlmodel import Session

engine = create_engine("sqlite:///database.db", echo=True)


def get_session():
    with Session(engine) as session:
        yield session
