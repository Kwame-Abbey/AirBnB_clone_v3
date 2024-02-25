#!/usr/bin/python3
"""Creates a route called status"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """Returns the status of api"""
    return jsonify({'status': 'OK'})
