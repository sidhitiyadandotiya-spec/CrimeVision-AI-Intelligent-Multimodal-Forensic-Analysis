"""Read-only Flask entry point for the public Vercel deployment."""
from flask import jsonify, request

from backend.flask_app import app


@app.before_request
def enforce_read_only_demo():
    if request.method not in {"GET", "HEAD", "OPTIONS"}:
        return jsonify({"error": "This public demo is read-only."}), 403
