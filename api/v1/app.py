#!/usr/bin/python3
"""Starts a flask web application"""

from flask import Flask
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)

HBNB_API_HOST = os.getenv("HBNB_API_HOST", "0.0.0.0")
HBNB_API_PORT = os.getenv("HBNB_API_PORT", 5000)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Closes storage"""
    storage.close()


if __name__ == '__main__':
    app.run(host=HBNB_API_HOST,
            port=HBNB_API_PORT,
            threaded=True)
