from flask import Flask
# lesson 3
from .db import db, migrate
from .models import book
from .routes.book_routes import books_bp


# lesson 1
# from .routes.hello_world_routes import hello_world_bp

# lesson 2
from .routes.book_routes import books_bp


def create_app():
    app = Flask(__name__)

    # lesson 1 - Register Blueprints here
    # app.register_blueprint(hello_world_bp)

    # lesson 3
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # connection string to our database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/hello_books_development'

    # connects to Flask app
    db.init_app(app)
    migrate.init_app(app, db)


    # lesson 2 - Register Blueprints here
    app.register_blueprint(books_bp)

    return app