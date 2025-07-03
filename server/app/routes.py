from flask import Blueprint, request, jsonify, current_app as app
from datetime import datetime, timedelta
from bson.json_util import dumps
from app.utils import parse_github_event
import logging
from dateutil.parser import parse as parse_datetime
import threading
import time

main_routes = Blueprint('main', __name__)

# Setup basic logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Background fetcher function
def fetch_recent_events(current_app_instance):
    with current_app_instance.app_context():
        while True:
            try:
                events_collection = current_app_instance.config["EVENTS_COLLECTION"]
                now = datetime.utcnow()
                time_threshold = now - timedelta(seconds=15)
                query = {"timestamp": {"$gte": time_threshold, "$lte": now}}
                
                # Fetch events, but don't log extensively to avoid cluttering logs
                events = list(events_collection.find(query).sort("timestamp", -1).limit(20))
                logger.info(f"Background fetcher: Fetched {len(events)} recent events.")
                
            except Exception as e:
                logger.error(f"❌ Error in background fetcher: {e}", exc_info=True)
            time.sleep(15) # Fetch every 15 seconds

# Start the background fetcher thread when the app starts
@main_routes.record_once
def on_load(state):
    # Ensure this runs only once when the app is ready
    if not hasattr(state.app, 'background_fetcher_started'):
        fetch_thread = threading.Thread(target=fetch_recent_events, args=(state.app,), daemon=True)
        fetch_thread.start()
        state.app.background_fetcher_started = True
        logger.info("Background fetcher thread started.")

@main_routes.route("/webhook", methods=["POST"])
def webhook():
    """
    Receives GitHub webhook events and stores them in MongoDB.
    Accepts PUSH, PULL_REQUEST, and MERGE events.
    """
    try:
        data = request.get_json()
        event_type = request.headers.get("X-GitHub-Event")

        parsed = parse_github_event(data, event_type)
        if not parsed:
            logger.warning(f"⚠️ Unhandled or invalid event: {event_type}")
            return jsonify({"error": f"Unhandled or invalid event: {event_type}"}), 400

        if "timestamp" in parsed and isinstance(parsed["timestamp"], str):
            parsed["timestamp"] = parse_datetime(parsed["timestamp"])
        elif not parsed.get("timestamp"):
            parsed["timestamp"] = datetime.utcnow()

        events_collection = app.config["EVENTS_COLLECTION"]
        events_collection.insert_one(parsed)

        logger.info(f"✅ Stored event: {parsed['action']} by {parsed['author']}")
        return jsonify({"message": "Event stored"}), 200

    except Exception as e:
        logger.error(f"❌ Webhook error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@main_routes.route("/events", methods=["GET"])
def get_events():
    """
    Fetches GitHub events from MongoDB.
    - If `?all=true` is passed, returns the latest 20 events.
    - Otherwise, returns events created within the last 15 seconds.
    """
    try:
        events_collection = app.config["EVENTS_COLLECTION"]
        
        fetch_all = request.args.get('all', 'false').lower() == 'true'
        
        query = {}
        if not fetch_all:
            now = datetime.utcnow()
            time_threshold = now - timedelta(seconds=15)
            query = {"timestamp": {"$gte": time_threshold, "$lte": now}}
            logger.info("🕒 Fetching recent events (last 15s)")
        else:
            logger.info("🕒 Fetching all events (limit 20)")

        results = list(events_collection.find(query).sort("timestamp", -1).limit(20))

        return app.response_class(
            response=dumps(results),
            status=200,
            mimetype="application/json"
        )
 
    except Exception as e:
        logger.error(f"❌ Fetching events failed: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500