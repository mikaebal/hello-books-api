# class Book:
#     def __init__(self, id, title, description):
#         self.id = id
#         self.title = title
#         self.description = description

# books = [
#     Book(1, "Fictional Book", "A fantasy novel set in an imaginary world."),
#     Book(2, "Wheel of Time", "A fantasy novel set in an imaginary world."),
#     Book(3, "Fictional Book Title", "A fantasy novel set in an imaginary world.")
# ]

# lesson 3 
from sqlalchemy.orm import Mapped, mapped_column, relationship

# L8 - (optional) 1 to many relationship
from sqlalchemy import ForeignKey
from typing import Optional

from ..db import db
# lesson 8 - removing warning underlines after creating relationship between models
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .author import Author


# Book is derived from db.Model
# db.Model is derived from DeclarativeBase
class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    # lesson 8 - connecting Book to Author
    # Foreign Key to child = author_id - L8 - (optional) 1 to many relationship
    author_id: Mapped[Optional[int]] = mapped_column(ForeignKey("author.id"))
    # adds attribute to author - if there is author then will be an instance of Author bc referencing class
    # if don't then return None bc it is optional
    # back_populates syncronizes with books
    author: Mapped[Optional["Author"]] = relationship(back_populates="books")


    # lesson 7

    # single instance of class Book (already exists)
    # dict representation
    # used to output a book instance (sending json to client)
    # doesn't create a new Book
    # Converts a Book object to a dictionary (output)
    def to_dict(self):
        book_as_dict = {}
        book_as_dict["id"] = self.id
        book_as_dict["title"] = self.title
        book_as_dict["description"] = self.description

        # L8 - handling nested routes! 
        if self.author:
            book_as_dict["author"] = self.author.name
        # check syntax- not right - book:self.book,name if self.id else None

        return book_as_dict
    


    # refering to class itself not the instance
    # creating new instances
    # build a new Book from input
    # Creates a Book object from a dictionary (input)
    @classmethod
    def from_dict(cls, book_data):

        # L8 - handling nested routes! 
        # Use get() to fetch values that could be undefined to avoid raising an error
        author_id = book_data.get("author_id")

        # adds author_id so we can use it in routes for POST
        new_book = cls(
            title=book_data["title"],
            description=book_data["description"],
            # if dict has this id then set it to the value. if not then it returns None
            author_id=author_id.get("author_id", None)
        )

        return new_book