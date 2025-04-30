import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
import os
from app.models.book import Book

# don't have to import conftest
# just bookkeeping purposes
# loads automatically when tests runs

load_dotenv()

# lets us create an app to use a test
# calls app: from app import create_app
@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    }
    app = create_app(test_config)
    # settings in test_config will be merged into the default configuration 
    # app.config, inside the create_app function

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove() # ensures update is reflected in db

    # designates application context
    with app.app_context():
        db.create_all()  # recreates tables needed for models
        yield app        # allows func to resume later on 

    with app.app_context():
        db.drop_all()

# register client fixture
@pytest.fixture
# makes a test client (simulate client making http request)
def client(app):
    return app.test_client() 


@pytest.fixture
def two_saved_books(app):
    # Arrange
    ocean_book = Book(title="Ocean Book",
                    description="watr 4evr")
    mountain_book = Book(title="Mountain Book",
                        description="i luv 2 climb rocks")

    db.session.add_all([ocean_book, mountain_book])
    # Alternatively, we could do
    # db.session.add(ocean_book)
    # db.session.add(mountain_book)
    db.session.commit()

