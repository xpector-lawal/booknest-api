
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Boolean, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


# SQLAlchemy model: defines the PostgreSQL books table
class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    author: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    is_available: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )


# Pydantic model: validates data submitted when creating a book
class BookCreate(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    price: Decimal = Field(gt=0)
    is_available: bool = True


# Pydantic model: defines the book data returned by the API
class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    author: str
    price: Decimal
    is_available: bool
