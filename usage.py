from sqlmodel import create_engine, Session, select
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from euro_core_backend.data.tag import Tag
from euro_core_backend.data.entry import Entry


def __main__() -> None:
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"

    engine = create_engine(sqlite_url, echo=True)

    with Session(engine) as session:
        #session.add(Tag(name="A"))
        #session.add(Tag(name="B"))
        tag_1 = session.exec(select(Tag).where(Tag.name == "A")).one()
        tag_2 = session.exec(select(Tag).where(Tag.name == "B")).one()
        #session.commit()

    entry_1 = Entry(
        name="Awesome Entry",
        url="https://aiddl.org",
        description="Language for Integrative AI",
        tags=[tag_1, tag_2])

    with Session(engine) as session:

        session.add(entry_1)

        session.commit()

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    url = 'http://127.0.0.1:8000'
    answer = session.get(f"{url}/entry/get/4")
    print(answer.status_code)
    print(answer.text)
    answer = session.get(f"{url}/tag/get/4")
    print(answer.status_code)
    print(answer.text)


if __name__ == "__main__":
    __main__()

