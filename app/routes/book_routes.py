from flask import Blueprint, abort, make_response, request, Response
from app.models.book import Book
from ..db import db

# define blueprint instance
books_bp = Blueprint("books_bp", __name__, url_prefix="/books")


# lesson 3 endpoint with flask
@books_bp.post("")
def create_book():
    request_body = request.get_json()
    title = request_body["title"]
    description = request_body["description"]

    # converting to python data type from json
    new_book = Book(title=title, description=description)
    db.session.add(new_book)
    db.session.commit()

    response = {
        "id": new_book.id,
        "title": new_book.title,
        "description": new_book.description,
    }
    return response, 201

@books_bp.get("")
def get_all_books():
    # lesson 5 refactor

    # Part 1 - building Select object
    # will always start by selecting book
    query = db.select(Book)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Book.title.ilike(f"%{title_param}%"))

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Book.description.ilike(f"%{description_param}%"))

    # Part 2 - update query by book id to whichever the query refers to above
    # will always end by ordering book id despite what happens in middle
    # book.id.desc() to desend order
    query = query.order_by(Book.id)

    books = db.session.scalars(query.order_by(Book.id))

    # lecture version
    # query = query.order_by(Cat.name)
    # books = db.session.scalars(query)

    # Learn version
    # query = db.select(Book).order_by(Book.id)
    # books = db.session.scalars(query)


    books_response = []
    for book in books:
        books_response.append(
            {
                "id": book.id,
                "title": book.title,
                "description": book.description
            }
        )
    return books_response


# lesson 4
@books_bp.get("/<book_id>")
def get_one_book(book_id):
    query = db.select(Book).where(Book.id == book_id)
    book = db.session.scalar(query)

    # lecture 
    # cat = validate_cat(id)

    return {
        "id": book.id,
        "title": book.title,
        "description": book.description
    }

# updating a book endpoint
@books_bp.put("/<book_id>")
def update_book(book_id):
    book = validate_book(book_id)
    request_body = request.get_json()

    # instance of Book, making changes in db Model
    book.title = request_body["title"]
    book.description = request_body["description"]
    db.session.commit()

    # import response 
    return Response(status=204, mimetype="application/json")

# deleting endpoint separately
@books_bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_book(book_id)
    db.session.delete(book)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        response = {"message": f"book {book_id} invalid"}
        abort(make_response(response , 400))

    query = db.select(Book).where(Book.id == book_id)
    book = db.session.scalar(query)
    
    if not book:
        response = {"message": f"book {book_id} not found"}
        abort(make_response(response, 404))

    return book





# lesson 2

# get_all_books hard coded book record
# @books_bp.get("")
# def get_all_books():
#     books_response = []
#     for book in books:
#         books_response.append(
#             {
#                 "id": book.id,
#                 "title": book.title,
#                 "description": book.description
#             }
#         )
#     return books_response

# hard coded book record
# @books_bp.get("/<book_id>")
# def get_one_book(book_id):
#     book = validate_book(book_id)

#     return {
#         "id": book.id,
#         "title": book.title,
#         "description": book.description,
#     }


# # helper function
# def validate_book(book_id):
#     try:
#         book_id = int(book_id)
#     except:
#         response = {"message": f"book {book_id} invalid"}
#         abort(make_response(response, 400))

#     for book in books:
#         if book.id == book_id:
#             return book

#     response = {"message": f"book {book_id} not found"}
#     abort(make_response(response, 404))
