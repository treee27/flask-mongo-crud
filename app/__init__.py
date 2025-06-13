from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.secret_key = "mySecret"
    app.config["MONGO_URI"] = "mongodb://localhost:27017/peoples"
    mongo.init_app(app)

    from app.routes.users import users_bp, api_bp
    app.register_blueprint(users_bp)
    app.register_blueprint(api_bp)

    return app
