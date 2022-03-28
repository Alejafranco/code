from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..dependencies import authenticate_token, get_session
from ..models import Item, ItemBase

router = APIRouter()


@router.post(
    "/users/{user_id}/items/",
    response_model=Item,
    dependencies=[Depends(authenticate_token)],
)
def create_item_for_user(
    user_id: int, item: ItemBase, session: Session = Depends(get_session)
):
    """
    Create an item for a specific user.
    """
    db_item = Item.from_orm(item, update={"user_id": user_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@router.get("/items/", response_model=List[Item])
def read_items(
    offset: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    """
    Read all the items. Doesn't need authentication.
    """
    items = session.exec(select(Item).offset(offset).limit(limit)).all()
    return items