from sqlmodel import Session, select
from database import Note as DBNote
from models import Note as APINote


class NoNoteFoundException(Exception):
    pass


def api_note_to_db(note: APINote) -> DBNote:
    return DBNote(
        title=note.title,
        content=note.content,
        create_date=note.create_date,
        modified_date=note.modified_date,
    )


def db_note_to_api(note: DBNote) -> APINote:
    return APINote(
        id=note.id,
        title=note.title,
        content=note.content,
        create_date=note.create_date,
        modified_date=note.modified_date,
    )


def create_note(db: Session, note: APINote) -> APINote:
    db_note = api_note_to_db(note)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note_to_api(db_note)


def query_note_by_title(db: Session, title: str) -> list[APINote]:
    db_notes = db.exec(select(DBNote).where(DBNote.title == title)).all()
    if not db_notes:
        raise NoNoteFoundException()
    return [db_note_to_api(db_note) for db_note in db_notes]


def query_all_notes(db: Session) -> list[APINote]:
    db_notes = db.exec(select(DBNote)).all()
    if not db_notes:
        raise NoNoteFoundException()
    return [db_note_to_api(db_note) for db_note in db_notes]
