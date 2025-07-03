import logging
from app import create_app

# Configure global logging before app starts
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for verbose logging
    format="%(asctime)s [%(levelname)s] in %(module)s: %(message)s"
)

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
