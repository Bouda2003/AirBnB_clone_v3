#!/usr/bin/python3
""" objects that handle all default RestFul API actions for States """
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.errorhandler(415)
def wrong_type(error):
    return make_response(jsonify({'error': 'Not a JSON'}), 400)


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """
    Retrieves the list of all State objects
    """
    if storage.get(Place, place_id) is None:
        abort(404)
    all_reviews = storage.all(Review).values()
    list_reviews = []
    for review in all_reviews:
        if review.to_dict()['place_id'] == place_id:
            list_reviews.append(review.to_dict())
    return jsonify(list_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ Retrieves a specific State """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(state_id):
    """
    Deletes a State Object
    """

    review = storage.get(Review, state_id)

    if not review:
        abort(404)

    storage.delete(review)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """
    Creates a State
    """
    if storage.get(Place, place_id) is None:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    if storage.get(User, request.get_json()['user_id']):
        abort(404)

    if 'text' not in request.get_json():
        abort(400, description="Missing text")

    data = request.get_json()
    data['place_id'] = place_id
    instance = State(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """
    Updates a State
    """
    review = storage.get(Review, review_id)

    if not state:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
