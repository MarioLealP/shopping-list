from uuid import UUID
from sqlmodel import Session, select
from database import (
    Note as DBNote,
    ShoppingList as DBShoppingList,
    ShoppingListItem as DBShoppingListItem,
)
from models import (
    Note as APINote,
    ShoppingList as APIShoppingList,
    ShoppingListItem as APIShoppingListItem,
)


class NoNoteFoundException(Exception):
    pass


class NoShoppingListFoundException(Exception):
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


def api_shopping_list_item_to_db(
    item: APIShoppingListItem, shopping_list_id: UUID
) -> DBShoppingListItem:
    return DBShoppingListItem(
        name=item.name,
        extra_info=item.extra_info,
        quantity=item.quantity,
        shopping_list_id=shopping_list_id,
    )


def db_shopping_list_item_to_api(item: DBShoppingListItem) -> APIShoppingListItem:
    return APIShoppingListItem(
        name=item.name,
        extra_info=item.extra_info,
        quantity=item.quantity,
    )


def api_shopping_list_to_db(shopping_list: APIShoppingList) -> DBShoppingList:
    db_shopping_list = DBShoppingList(
        name=shopping_list.name,
    )
    return db_shopping_list


def db_shopping_list_to_api(
    shopping_list: DBShoppingList, items: list[DBShoppingListItem]
) -> APIShoppingList:
    return APIShoppingList(
        name=shopping_list.name,
        items=[db_shopping_list_item_to_api(item) for item in items],
    )


def create_shopping_list_item(
    db: Session, item: APIShoppingListItem, shopping_list_id: UUID
) -> APIShoppingListItem:
    db_item = api_shopping_list_item_to_db(item, shopping_list_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_shopping_list_item_to_api(db_item)


def create_shopping_list(
    db: Session, shopping_list: APIShoppingList
) -> APIShoppingList:
    db_shopping_list = api_shopping_list_to_db(shopping_list)
    db.add(db_shopping_list)
    db.commit()
    db.refresh(db_shopping_list)

    shopping_list_items = []

    for item in shopping_list.items:
        db_item = api_shopping_list_item_to_db(item, db_shopping_list.id)
        db.add(db_item)
        shopping_list_items.append(db_item)

    db.commit()

    return db_shopping_list_to_api(db_shopping_list, shopping_list_items)


def query_all_shopping_lists(db: Session) -> list[APIShoppingList]:
    db_shopping_lists = db.exec(select(DBShoppingList)).all()
    if not db_shopping_lists:
        raise NoNoteFoundException()

    shopping_lists = []
    for db_shopping_list in db_shopping_lists:
        items = list(
            db.exec(
                select(DBShoppingListItem).where(
                    DBShoppingListItem.shopping_list_id == db_shopping_list.id
                )
            ).all()
        )
        shopping_lists.append(db_shopping_list_to_api(db_shopping_list, items))

    return shopping_lists


def query_shopping_list_by_name(db: Session, name: str) -> APIShoppingList:
    db_shopping_list = db.exec(
        select(DBShoppingList).where(DBShoppingList.name == name)
    ).first()
    if not db_shopping_list:
        raise NoShoppingListFoundException()

    items = list(
        db.exec(
            select(DBShoppingListItem).where(
                DBShoppingListItem.shopping_list_id == db_shopping_list.id
            )
        ).all()
    )
    return db_shopping_list_to_api(db_shopping_list, items)
