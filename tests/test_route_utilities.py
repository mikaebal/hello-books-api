from werkzeug.exceptions import HTTPException
from app.routes.route_utilities import validate_model
import pytest
from app.models.book import Book

# test validate_book from book routes

def test_validate_model(two_saved_books):
    # Act
    result_book = validate_model(Book, 1)

    # Assert
    assert result_book.id == 1
    assert result_book.title == "Ocean Book"
    assert result_book.description == "watr 4evr"

def test_validate_model_missing_record(two_saved_books):
    # Act & Assert
    # Calling `validate_model` without being invoked by a route will
    # cause an `HTTPException` when an `abort` statement is reached 
    with pytest.raises(HTTPException):
        result_book = validate_model(Book, "3")
    
def test_validate_model_invalid_id(two_saved_books):
    # Act & Assert
    # Calling `validate_model` without being invoked by a route will
    # cause an `HTTPException` when an `abort` statement is reached 
    with pytest.raises(HTTPException):
        result_book = validate_model(Book, "cat")


# similar
def test_validate_book_missing_record(two_saved_books):
    # Act & Assert
    # Calling `validate_book` without being invoked by a route will
    # cause an `HTTPException` when an `abort` statement is reached 
    with pytest.raises(HTTPException):
        result_book = validate_book("3")
    
def test_validate_book_invalid_id(two_saved_books):
    # Act & Assert
    # Calling `validate_book` without being invoked by a route will
    # cause an `HTTPException` when an `abort` statement is reached 
    with pytest.raises(HTTPException):
        result_book = validate_book("cat")