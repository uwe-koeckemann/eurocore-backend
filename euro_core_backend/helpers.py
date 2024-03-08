from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlmodel import select


def get_by_id(session, db_id, data_type):
    data = session.get(data_type, db_id)
    if not data:
        raise HTTPException(status_code=404, detail=f"No {data_type.__name__} row found with ID: {db_id}")
    return data


def get_by_name(session, name, data_type):
    try:
        tag = session.exec(select(data_type).where(data_type.name == name)).one()
        return tag
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"No {data_type.__name__} row found with name: {name}")


def create(session, data, data_type):
    db_data = data_type.model_validate(data)
    session.add(db_data)
    session.commit()
    return db_data


def update(session, row, db_type):
    db_row = session.get(db_type, row.id)
    if not db_row:
        raise HTTPException(status_code=404, detail=f"{db_type.__name__} not found. Could not update {row}")
    row_data = row.dict(exclude_unset=True)
    for key, value in row_data.items():
        setattr(db_row, key, value)
    session.add(db_row)
    session.commit()
    session.refresh(db_row)
    return db_row


def delete(session, row_id, db_type):
    db_row = session.get(db_type, row_id)
    if not db_row:
        raise HTTPException(status_code=404, detail=f"Cannot delete {db_row} from {db_type.__name__}: not found")
    # TODO: Add constraints that may forbid delete of linked data or perform additional deletes
    session.delete(db_row)
    session.commit()
    return db_row


def assert_exists(session, row_id, db_type):
    db_row = session.get(db_type, row_id)
    if not db_row:
        raise HTTPException(status_code=404, detail=f"Could not find {db_type.__name__} with id: {row_id}")