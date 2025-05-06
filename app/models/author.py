from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
# lesson 8 - removing warning underlines after creating relationship between models
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .author import Book

class Author(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    # lesson 8 - connecting(database connection) Author to Book 
    # these will be OBJECT instances representations of models 
    books: Mapped[list["Book"]] = relationship(back_populates="author")

    # makes instance of class
    def to_dict(self):
        author_as_dict = {
            "id": self.id,
            "name": self.name
        }
        
        return author_as_dict
    
    # refers to class itself, but make a new instance "new_autor" to call it 
    @classmethod
    def from_dict(cls, author_data):
        new_author = cls(name=author_data["name"])
        return new_author