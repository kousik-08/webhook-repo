from datetime import datetime

def parse_github_event(data, event_type):
    if event_type == "push":
        return {
            "request_id": data.get("after"),
            "author": data.get("pusher", {}).get("name"),
            "action": "PUSH",
            "from_branch": data.get("ref", "").split("/")[-1],
            "to_branch": data.get("ref", "").split("/")[-1],
            "timestamp": data.get("head_commit", {}).get("timestamp")
        }

    elif event_type == "pull_request":
        pr = data.get("pull_request", {})
        return {
            "request_id": str(pr.get("id")),
            "author": pr.get("user", {}).get("login"),
            "action": "MERGE" if pr.get("merged") else "PULL_REQUEST",
            "from_branch": pr.get("head", {}).get("ref"),
            "to_branch": pr.get("base", {}).get("ref"),
            "timestamp": pr.get("updated_at")
        }

    return None
