import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient
from app.routes import main_routes

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Mongo Setup
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGO_DB", "webhookDB")
    client = MongoClient(mongo_uri)
    db = client[db_name]
    app.config["EVENTS_COLLECTION"] = db["events"]

    # Register routes
    app.register_blueprint(main_routes)

    return app
