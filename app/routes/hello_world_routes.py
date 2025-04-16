from flask import Blueprint

hello_world_bp = Blueprint("hello_world", __name__)

# endpoint 1
@hello_world_bp.get("/")
def say_hello_world():
    return "Hello, World!"

# endpoint 2
@hello_world_bp.get("/hello/JSON")
def say_hello_json():
    return {
        "name": "Ada Lovelace",
        "message": "Hello!",
        "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
    }

# endpoint 3 (debugged)
@hello_world_bp.get("/broken-endpoint-with-broken-server-code")
def broken_endpoint():
    response_body = {
        "name": "Ada Lovelace",
        "message": "Hello!",
        "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
    }
    new_hobby = ["Surfing"]
    response_body["hobbies"] + new_hobby
    return response_body