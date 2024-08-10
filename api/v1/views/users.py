#!/usr/bin/python3
""" objects that handle all default RestFul API actions for States """
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.errorhandler(415)
def wrong_type(error):
    return make_response(jsonify({'error': 'Not a JSON'}), 400)


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves the list of all State objects
    """
    all_states = storage.all(User).values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/users/<state_id>', methods=['GET'], strict_slashes=False)
def get_user(state_id):
    """ Retrieves a specific State """
    state = storage.get(User, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/users/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(state_id):
    """
    Deletes a State Object
    """

    state = storage.get(User, state_id)

    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """
    Creates a State
    """
    if not request.get_json():
        abort(400, "Not a JSON")

    if 'email' not in request.get_json():
        abort(400, description="Missing email")

    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    data = request.get_json()
    instance = User(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/users/<state_id>', methods=['PUT'], strict_slashes=False)
def put_user(state_id):
    """
    Updates a State
    """
    state = storage.get(User, state_id)

    if not state:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at', 'email']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
