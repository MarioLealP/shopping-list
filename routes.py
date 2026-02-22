from tkinter import N
from sqlmodel import Session
from database import engine
from models import (
    ResponseListNotes,
    Note,
    NoteTitle,
    ResponseNote,
    NoteNotFoundError,
    ErrorResponse,
)
from fastapi import FastAPI
from queries import (
    create_note,
    query_note_by_title,
    query_all_notes,
    NoNoteFoundException,
)

app = FastAPI()


@app.post(
    "/note",
    tags=["Note"],
    summary="Create a new note",
    description="Creates a new note with the provided title and content.",
    responses={
        201: {"description": "The created note", "model": ResponseNote},
        400: {"description": "Invalid input"},
    },
)
def new_note(note: Note) -> ResponseNote:
    with Session(engine) as session:
        created_note = create_note(session, note)
    return ResponseNote(note=created_note)


@app.get(
    "/notes",
    tags=["Note"],
    summary="Get all notes",
    description="Retrieves a list of all notes.",
    responses={
        200: {"description": "A list of notes", "model": ResponseListNotes},
        404: {"description": "No notes found", "model": ErrorResponse},
    },
)
def get_all_notes() -> ResponseListNotes:
    try:
        with Session(engine) as session:
            notes = query_all_notes(session)
            return ResponseListNotes(notes=notes)
    except NoNoteFoundException:
        raise NoteNotFoundError(status_code=404, detail="No notes found")


@app.get(
    "/note",
    tags=["Note"],
    summary="Get a note by title",
    description="Retrieves a note by its title.",
    responses={
        200: {"description": "The requested note", "model": ResponseNote},
        404: {"description": "Note not found", "model": ErrorResponse},
    },
)
def get_note_by_title(title: NoteTitle) -> ResponseListNotes:
    try:
        with Session(engine) as session:
            notes = query_note_by_title(session, title)
        return ResponseListNotes(notes=notes)
    except NoNoteFoundException:
        raise NoteNotFoundError(
            status_code=404, detail=f"No note found with title '{title}'"
        )
