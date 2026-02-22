from fastapi import HTTPException
from typing import List, Annotated, TypeAlias, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from uuid import UUID

NoteTitle: TypeAlias = Annotated[
    str, Field(examples=["My Note Title"], description="The title of the note")
]


class Note(BaseModel):
    id: Optional[UUID] = Field(
        None,
        examples=["123e4567-e89b-12d3-a456-426614174000"],
        description="The unique identifier for the note",
    )
    title: NoteTitle
    content: str = Field(
        examples=["This is the content of the note."],
        description="The content of the note",
    )
    create_date: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc),
        examples=["2024-06-01T12:00:00Z"],
        description="The date and time when the note was created",
    )
    modified_date: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc),
        examples=["2024-06-01T12:00:00Z"],
        description="The date and time when the note was last modified",
    )


class ResponseListNotes(BaseModel):
    notes: List[Note]


class ResponseNote(BaseModel):
    note: Note


class ErrorResponse(BaseModel):
    detail: str = Field(description="Error message")


class NoteNotFoundError(HTTPException):
    pass
