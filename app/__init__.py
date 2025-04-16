from flask import Flask

# lesson 1
# from .routes.hello_world_routes import hello_world_bp

# lesson 2
from .routes.book_routes import books_bp


def create_app():
    app = Flask(__name__)

    # lesson 1 - Register Blueprints here
    # app.register_blueprint(hello_world_bp)

    # lesson 2 - Register Blueprints here
    app.register_blueprint(books_bp)

    return app