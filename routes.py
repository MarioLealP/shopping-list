from sqlmodel import Session
from database import engine
from models import (
    ResponseListNotes,
    Note,
    NoteTitle,
    ResponseNote,
    NoteNotFoundError,
    ErrorResponse,
    ShoppingList,
    ResponseShoppingList,
    ResponseListShoppingLists,
    ShoppingListNotFoundError,
)
from fastapi import FastAPI
from queries import (
    create_note,
    query_note_by_title,
    query_all_notes,
    NoNoteFoundException,
    create_shopping_list,
    query_all_shopping_lists,
    NoShoppingListFoundException,
    query_shopping_list_by_name,
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


@app.post(
    "/shopping-list",
    tags=["Shopping List"],
    summary="Create a new shopping list",
    description="Creates a new shopping list with the provided name and items.",
    responses={
        201: {
            "description": "The created shopping list",
            "model": ResponseShoppingList,
        },
        400: {"description": "Invalid input"},
    },
)
def new_shopping_list(shopping_list: ShoppingList) -> ResponseShoppingList:
    with Session(engine) as session:
        created_shopping_list = create_shopping_list(session, shopping_list)
    return ResponseShoppingList(shopping_list=created_shopping_list)


@app.get(
    "/shopping-lists",
    tags=["Shopping List"],
    summary="Get all shopping lists",
    description="Retrieves a list of all shopping lists.",
    responses={
        200: {
            "description": "A list of shopping lists",
            "model": ResponseListShoppingLists,
        },
        404: {"description": "No shopping lists found", "model": ErrorResponse},
    },
)
def get_all_shopping_lists() -> ResponseListShoppingLists:
    try:
        with Session(engine) as session:
            shopping_lists = query_all_shopping_lists(session)
            return ResponseListShoppingLists(shopping_lists=shopping_lists)
    except NoShoppingListFoundException:
        raise ShoppingListNotFoundError(
            status_code=404, detail="No shopping lists found"
        )


@app.get(
    "/shopping-list",
    tags=["Shopping List"],
    summary="Get a shopping list by name",
    description="Retrieves a shopping list by its name.",
    responses={
        200: {
            "description": "The requested shopping list",
            "model": ResponseShoppingList,
        },
        404: {"description": "Shopping list not found", "model": ErrorResponse},
    },
)
def get_shopping_list_by_name(name: str) -> ResponseShoppingList:
    try:
        with Session(engine) as session:
            shopping_lists = query_shopping_list_by_name(session, name)
            if not shopping_lists:
                raise NoShoppingListFoundException()
            return ResponseShoppingList(shopping_list=shopping_lists)
    except NoShoppingListFoundException:
        raise ShoppingListNotFoundError(
            status_code=404, detail=f"No shopping list found with name '{name}'"
        )
