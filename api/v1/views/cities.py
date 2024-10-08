#!/usr/bin/python3
""" objects that handle all default RestFul API actions for States """
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities_of_state(state_id):
    """gets all cities of a certain state"""
    if storage.get(State, state_id) is None:
        abort(404)
    cities = storage.all(City).values()
    state_cities = []
    for city in cities:
        if city.to_dict()['state_id'] == state_id:
            state_cities.append(city.to_dict())
    return jsonify(state_cities)


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def get_cities():
    """
    Retrieves the list of all State objects
    """
    all_states = storage.all(City).values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/cities/<state_id>', methods=['GET'], strict_slashes=False)
def get_city(state_id):
    """ Retrieves a specific State """
    state = storage.get(City, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/cities/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_cities(state_id):
    """
    Deletes a State Object
    """

    state = storage.get(City, state_id)

    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_cities(state_id):
    """
    Creates a City
    """
    if not request.get_json():
        abort(400, "Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    if storage.get(State, state_id) is None:
        abort(404)
    data = request.get_json()
    instance = City(**data)
    instance.state_id = state_id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/cities/<state_id>', methods=['PUT'], strict_slashes=False)
def put_cites(state_id):
    """
    Updates a State
    """
    state = storage.get(City, state_id)

    if not state:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at', 'state_id']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
