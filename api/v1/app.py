#!/usr/bin/python3
"""Starts a flask web application"""

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Closes storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handler for 404 errors"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    HBNB_API_HOST = os.getenv("HBNB_API_HOST", "0.0.0.0")
    HBNB_API_PORT = os.getenv("HBNB_API_PORT", 5000)
    app.run(host=HBNB_API_HOST,
            port=HBNB_API_PORT,
            threaded=True)
