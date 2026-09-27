"""
WSGI Entry Point for Cloud Deployment (Render, PythonAnywhere, Railway, Gunicorn).
"""
import os
from app import app

# Ensure SQLite is used if deploying on cloud platforms
if not os.getenv("DB_TYPE"):
    os.environ["DB_TYPE"] = "sqlite"

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
