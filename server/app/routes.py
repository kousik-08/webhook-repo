from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from app.utils import parse_github_event

main_routes = Blueprint('main', __name__)

@main_routes.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        event_type = request.headers.get("X-GitHub-Event")

        parsed = parse_github_event(data, event_type)
        if not parsed:
            return jsonify({"error": f"Unhandled or invalid event: {event_type}"}), 400

        if not parsed.get("timestamp"):
            parsed["timestamp"] = datetime.utcnow().isoformat()

        events_collection = current_app.config["EVENTS_COLLECTION"]
        events_collection.insert_one(parsed)

        return jsonify({"message": "Event stored"}), 200

    except Exception as e:
        current_app.logger.error(f"Webhook error: {e}")
        return jsonify({"error": str(e)}), 500


@main_routes.route("/events", methods=["GET"])
def get_events():
    try:
        events_collection = current_app.config["EVENTS_COLLECTION"]
        results = list(events_collection.find().sort("timestamp", -1).limit(20))
        for doc in results:
            doc["_id"] = str(doc["_id"])
        return jsonify(results)

    except Exception as e:
        current_app.logger.error(f"Fetching events failed: {e}")
        return jsonify({"error": str(e)}), 500


#NEW git update