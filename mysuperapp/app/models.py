from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class ItemBase(SQLModel):
    title: str
    description: Optional[str] = None


class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")

    user: Optional["User"] = Relationship(back_populates="items")


class UserBase(SQLModel):
    username: str


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    is_active: bool = True
    items: List[Item] = Relationship(back_populates="user")


class UserWithItems(UserBase):
    id: int
    is_active: bool
    items: List[Item]