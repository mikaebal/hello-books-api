from flask import Blueprint, request, make_response, abort
from app.models.author import Author
from ..db import db
from .route_utilities import validate_model, create_model, get_models_with_filters

# convention name for decoratators in blueprint is just bp
# but authors_bp needs to be unique for eternal tracking
# this is instance of Blueprint
bp = Blueprint("authors_bp", __name__, url_prefix="/authors")

@bp.post("")
def create_author():
    request_body = request.get_json()
    return create_model(Author, request_body)

    # without helper function create_model
    # try:
    #     new_author = Author.from_dict(request_body)
        
    # except KeyError as error:
    #     response = {"message": f"Invalid request: missing {error.args[0]}"}
    #     abort(make_response(response, 400))
    
    # # if try, except is successful then this happens
    # db.session.add(new_author)
    # db.session.commit()

    # return make_response(new_author.to_dict(), 201)

@bp.get("")
def get_all_authors():
    return get_models_with_filters(Author, request.args)

    # query = db.select(Author)

    # name_param = request.args.get("name")
    # if name_param:
    #     query = query.where(Author.name.ilike(f"%{name_param}%"))

    # # if there is a Author then scalars happens 

    # authors = db.session.scalars(query.order_by(Author.id))
    # # Use list comprehension syntax to create the list `authors_response`
    # authors_response = [author.to_dict() for author in authors]

    # return authors_response


# L8- nested route
@bp.post("/<author_id>/books")
def create_book_with_author(author_id):
    author = validate_model(Author, author_id)
    
    request_body = request.get_json()
    request_body["author_id"] = author.id
    return create_model(Book, request_body)

    # without helper function create_model
    # request_body = request.get_json()
    # request_body["author_id"] = author.id

    # try:
    #     new_book = Book.from_dict(request_body)

    # except KeyError as e:
    #     response = {"message": f"Invalid request: missing {error.args[0]}"}
    #     abort(make_response(response, 400))
        
    # db.session.add(new_book)
    # db.session.commit()

    # return make_response(new_book.to_dict(), 201)

# getting all books from author
@bp.get("/<author_id>/books")
def get_books_by_author(author_id):
    author = validate_model(Author, author_id)
    # list comprehension
    response = [book.to_dict() for book in author.books]
    return response