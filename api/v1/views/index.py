#!/usr/bin/python3
"""Creates a route called status"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """Returns the status of api"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def get_stats():
    """Retrieves the number of each objects by type"""
    classes = ['Amenity', 'City', 'Place', 'Review', 'State', 'User']
    names = ['amenities', 'cities', 'places', 'reviews', 'states', 'users']
    stats = {}

    for idx, cls in enumerate(classes):
        stats[names[idx]] = storage.count(cls)
    return jsonify(stats)
