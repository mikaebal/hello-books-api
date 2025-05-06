from flask import Flask
# lesson 3
from .db import db, migrate
from .models import book, author
# from .routes.book_routes import books_bp
# lesson 6
import os
# lesson 7
from .routes.book_routes import bp as books_bp
# lesson 8 - creating an alias with as bc can't have 2 bps
from .routes.author_routes import bp as authors_bp


# lesson 1
# from .routes.hello_world_routes import hello_world_bp

# lesson 2
from .routes.book_routes import books_bp

# lesson 6 add config as param
def create_app(config=None):
    app = Flask(__name__)   # builds app

    # lesson 1 - Register Blueprints here
    # app.register_blueprint(hello_world_bp)

    # lesson 3
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   # disables unnessary features
    # connection string to our database
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/hello_books_development'
    
    # Lesson 6 refactor - sets value from development database in .env
    # reads SQLALCHEMY_DATABASE_URI value from .env file 
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI') 

    if config:
        # Merge `config` into the app's configuration
        # to override the app's default settings
        app.config.update(config)

    # Connects SQLAlchemy to Flask app
    db.init_app(app)
    # Connects Flask-Migrate to app and db
    migrate.init_app(app, db)


    # lesson 2 - Register Blueprints here
    app.register_blueprint(books_bp)
    # lesson 8 - register author bp !!
    app.register_blueprint(authors_bp)

    return app