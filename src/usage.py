from sqlmodel import create_engine, Session, select

from data.tag import Tag
from data.entry import Entry


def __main__() -> None:
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"

    engine = create_engine(sqlite_url, echo=True)

    with Session(engine) as session:
        statement = select(Tag).where(Tag.name == "A")
        tag_1 = session.exec(statement).one()
        tag_2 = session.exec(select(Tag).where(Tag.name == "B")).one()

    entry_1 = Entry(
        name="Awesome Entry",
        url="https://aiddl.org",
        description="Language for Integrative AI",
        tags=[tag_1, tag_2])

    with Session(engine) as session:
        #session.add(tag_1)
        #session.add(tag_2)
        session.add(entry_1)

        session.commit()


if __name__ == "__main__":
    __main__()