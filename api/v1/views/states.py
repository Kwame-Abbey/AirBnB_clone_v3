#!/usr/bin/python3
"""Create a new view for State objects that handles all
default RESTFul API actions
"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, jsonify, make_response, request


@app_views.route('/states', methods=['GET'])
def get_states():
    """Retrieves list of all State objects"""
    all_states = []
    all_objects = storage.all(State).values()
    for state in all_objects:
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'])
def create_state():
    """Creates a State"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    data = request.get_json()
    new_instance = State(**data)
    new_instance.save()

    return make_response(jsonify(new_instance.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()

    keys_to_ignore = ['id', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in keys_to_ignore:
            setattr(state, k, v)
    storage.save()

    return make_response(jsonify(state.to_dict()), 200)
