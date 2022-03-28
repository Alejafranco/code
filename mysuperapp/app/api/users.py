from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..dependencies import authenticate_token, get_session
from ..models import User, UserBase, UserWithItems

router = APIRouter()


@router.post(
    "/users/",
    response_model=User,
    dependencies=[Depends(authenticate_token)],
)
def create_user(user: UserBase, session: Session = Depends(get_session)):
    """
    Create a new user.
    """
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = User.from_orm(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/users/", response_model=List[User])
def read_users(
    offset: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    """
    Read users.

    Doesn't require authentication.
    """
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@router.get("/users/{user_id}", response_model=UserWithItems)
def read_user(user_id: int, session: Session = Depends(get_session)):
    """
    Read the data for a specific user.

    Doesn't require authentication.
    """
    db_user = session.exec(select(User).where(User.id == user_id)).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user