# from flask import Blueprint, request, jsonify, current_app
# from datetime import datetime
# from app.utils import parse_github_event

# main_routes = Blueprint('main', __name__)

# @main_routes.route("/webhook", methods=["POST"])
# def webhook():
#     try:
#         data = request.get_json()
#         event_type = request.headers.get("X-GitHub-Event")

#         parsed = parse_github_event(data, event_type)
#         if not parsed:
#             return jsonify({"error": f"Unhandled or invalid event: {event_type}"}), 400

#         if not parsed.get("timestamp"):
#             parsed["timestamp"] = datetime.utcnow().isoformat()

#         events_collection = current_app.config["EVENTS_COLLECTION"]
#         events_collection.insert_one(parsed)

#         return jsonify({"message": "Event stored"}), 200

#     except Exception as e:
#         current_app.logger.error(f"Webhook error: {e}")
#         return jsonify({"error": str(e)}), 500


# @main_routes.route("/events", methods=["GET"])
# def get_events():
#     try:
#         events_collection = current_app.config["EVENTS_COLLECTION"]
#         results = list(events_collection.find().sort("timestamp", -1).limit(20))
#         for doc in results:
#             doc["_id"] = str(doc["_id"])
#         return jsonify(results)

#     except Exception as e:
#         current_app.logger.error(f"Fetching events failed: {e}")
#         return jsonify({"error": str(e)}), 500


# #NEW git update

from flask import Blueprint, request, jsonify, current_app as app
from datetime import datetime, timedelta
from bson.json_util import dumps
from app.utils import parse_github_event
import logging
from dateutil.parser import parse as parse_datetime

main_routes = Blueprint('main', __name__)

# Setup basic logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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

        # Ensure timestamp is a datetime object
        if "timestamp" in parsed and isinstance(parsed["timestamp"], str):
            parsed["timestamp"] = parse_datetime(parsed["timestamp"].replace("Z", "+00:00"))
        elif not parsed.get("timestamp"):
            parsed["timestamp"] = datetime.utcnow()

        # Insert into MongoDB
        events_collection = app.config["EVENTS_COLLECTION"]
        events_collection.insert_one(parsed)

        logger.info(f"✅ Stored event: {parsed['action']} by {parsed['author']}")
        return jsonify({"message": "Event stored"}), 200

    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
        return jsonify({"error": str(e)}), 500

@main_routes.route("/events", methods=["GET"])
def get_events():
    """
    Fetches GitHub events from MongoDB.

    - If `?all=true` is passed, returns the latest 20 events.
    - Otherwise, returns events created within the last 15 seconds.
    Assumes `timestamp` is a `datetime` object in MongoDB.
    """
    try:
        events_collection = app.config["EVENTS_COLLECTION"]
        show_all = request.args.get("all", "false").lower() == "true"

        if show_all:
            query = {}
            logger.info("📥 Fetching latest 20 events (no time filter)")
        else:
            now = datetime.utcnow()
            time_threshold = now - timedelta(seconds=15)
            query = {
                "timestamp": {
                    "$gte": time_threshold,
                    "$lte": now
                }
            }
            logger.info(f"🕒 Fetching events from {time_threshold.isoformat()} to {now.isoformat()}")

        results = list(events_collection.find(query).sort("timestamp", -1).limit(20))

        return app.response_class(
            response=dumps(results),
            status=200,
            mimetype="application/json"
        )

    except Exception as e:
        logger.error(f"❌ Fetching events failed: {e}")
        return jsonify({"error": str(e)}), 500


