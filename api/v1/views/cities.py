#!/usr/bin/python3
"""create a new view for City objects that handles all
default RESTFul API actions
"""

from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Retrieves list of all City Objects
    of a State
    """
    cities_list = []
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for city in state.cities:
        cities_list.append(city.to_dict())

    return jsonify(cities_list)


@app_views.route('/cities/<city_id>/', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a specific city based on id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a city based on id provided"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)
    storage.delete(city)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = City(**data)
    instance.state_id = state.id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
