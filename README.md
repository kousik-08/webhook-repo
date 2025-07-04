# GitHub Webhook Receiver

A lightweight Flask application that listens for GitHub webhook events (`push`, `pull_request`, `merge`), stores them in MongoDB, and exposes an API endpoint to fetch the latest activity.

---

## 🚀 Features

- Receives GitHub Webhook events
- Stores data in MongoDB with structured schema
- Provides `/events` endpoint to fetch the latest 20 events
- Ready to be used with a React frontend or any polling client
- Built with separation of concerns using Flask Blueprints


---

## 🔧 Prerequisites

- Python 3.8+
- MongoDB (local or cloud, e.g., MongoDB Atlas)
- [ngrok](https://ngrok.com) (for testing webhooks locally)

---

## ⚙️ Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/kousik-08/webhook-repo.git
cd webhook-repo
```
2. Create and Activate a Virtual Environment

# Install virtualenv if not installed
```bash
python -m venv venv
```
# Create and activate the environment


# On Linux/macOS
```bash
source venv/bin/activate
```

# On Windows
```bash
venv\Scripts\activate
```

3. Install Required Packages
```bash
pip install -r requirements.txt
```

4. Configure Environment Variables

Create a .env file in the root directory:
```bash
MONGO_URI=mongodb://localhost:27017
MONGO_DB=webhookDB
```

5. Run the Flask Server
```bash
python run.py
```

🌐 Webhook Configuration (GitHub)
Go to your GitHub repository → Settings → Webhooks → Add webhook

Payload URL: http://<your-ngrok-url>/webhook

Content Type: application/json

Select events:
✅ Push events
✅ Pull request events
✅ (Optional) Merge events (implied by pull_request with merged = true)

ngrok http 5000

# GitHub Webhook Frontend

A responsive and dark-themed React frontend that connects to a Flask backend to display GitHub webhook activity in real-time. Events include `push`, `pull_request`, and `merge`, updated every 15 seconds.

---

## 🚀 Features

- React app with auto-refresh every 15 seconds
- Responsive dark UI design
- Displays GitHub activity in human-readable format
- Easily integrates with Flask + MongoDB backend

---

1. Install Dependencies
```bash
npm install
```
2. Start the Development Server
```bash
npm start
```

# webhook-repo
