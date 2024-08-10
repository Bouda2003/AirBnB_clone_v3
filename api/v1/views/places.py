#!/usr/bin/python3
""" objects that handle all default RestFul API actions for States """
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.errorhandler(415)
def wrong_type(error):
    return make_response(jsonify({'error': 'Not a JSON'}), 400)


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """
    Retrieves the list of all State objects
    """
    if storage.get(City, city_id) is None:
        abort(404)
    all_places = storage.all(Place).values()
    list_places = []
    for place in all_places:
        if place.to_dict()['city_id'] == city_id:
            list_places.append(place.to_dict())
    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieves a specific State """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(state_id):
    """
    Deletes a State Object
    """

    state = storage.get(Place, state_id)

    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """
    Creates a State
    """
    if storage.get(City, city_id) is None:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    if storage.get(User, request.get_json()['user_id']) is None:
        abort(404)

    data = request.get_json()
    data['city_id'] = city_id
    instance = Place(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/places/<state_id>', methods=['PUT'], strict_slashes=False)
def put_place(state_id):
    """
    Updates a State
    """
    state = storage.get(Place, state_id)

    if not state:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at', 'city_id', 'user_id']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
