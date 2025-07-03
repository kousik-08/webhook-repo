import os
import logging
from flask import Flask
from pymongo import MongoClient

# Setup basic logger
logger = logging.getLogger(__name__)

def create_app():
    """Creates and configures a Flask application instance."""
    app = Flask(__name__)

    # --- Database Configuration ---
    mongo_uri = os.environ.get("MONGO_URI")
    if not mongo_uri:
        logger.error("❌ MONGO_URI environment variable not set.")
        exit(1)

    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ismaster')
        logger.info(f"✅ Successfully connected to MongoDB using URI: {mongo_uri}")
        
        # Extract database name from URI or use a default
        db_name = mongo_uri.split('/')[-1].split('?')[0] if '/' in mongo_uri else "webhook_db"
        db = client[db_name]
        app.config["EVENTS_COLLECTION"] = db["events"]
    except Exception as e:
        logger.error(f"❌ Could not connect to MongoDB: {e}")
        # Exit if DB connection fails, as the app is useless without it.
        exit(1)

    # --- Register Blueprints ---
    from .routes import main_routes
    app.register_blueprint(main_routes)

    return app