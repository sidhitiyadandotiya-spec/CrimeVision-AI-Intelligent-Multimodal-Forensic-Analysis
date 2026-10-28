"""Vercel Serverless Function entry point for CrimeVision AI."""
import os
import sys
from pathlib import Path

# Ensure project root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Enforce read-only mode for public serverless deployment
os.environ["CRIMEVISION_READ_ONLY_DEMO"] = "1"

from flask import jsonify, request
from backend.flask_app import app

@app.before_request
def enforce_read_only_demo():
    if request.method not in {"GET", "HEAD", "OPTIONS"}:
        return jsonify({"error": "This public demo is read-only."}), 403

# Vercel Serverless automatically exposes 'app'
