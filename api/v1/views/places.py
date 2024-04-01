#!/usr/bin/python3
"""Places view API request handlers
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.user import User
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'], strict_slashes=False)
def places_by_city_requests(city_id):
    """Perform API requests of places by city
    """
    # GET REQUESTS
    if request.method == 'GET':
        cities = storage.all(City)
        try:
            key = 'City.' + city_id
            city = cities[key]
            place_list = [place.to_dict() for place in city.places]
            return jsonify(place_list)
        except KeyError:
            abort(404)

    # POST REQUESTS
    elif request.method == 'POST':
        cities = storage.all(City)
        if ('City.' + city_id) not in cities.keys():
            abort(404)

        if request.is_json:
            body_request = request.get_json()
        else:
            abort(400, 'Not a JSON')

        if 'name' not in body_request:
            abort(400, 'Missing name')
        if 'user_id' not in body_request:
            abort(400, 'Missing user_id')

        users = storage.all(User)
        if ('User.' + body_request['user_id']) not in users.keys():
            abort(404)

        body_request.update({'city_id': city_id})
        new_place = Place(**body_request)
        storage.new(new_place)
        storage.save()
        return jsonify(new_place.to_dict()), 201

    # UNSUPPORTED REQUESTS
    else:
        abort(501)


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def place_methods(place_id=None):
    """Perform API requests of on place objects
    """
    # GET REQUESTS
    if request.method == 'GET':
        places = storage.all(Place)
        try:
            key = 'Place.' + place_id
            place = places[key]
            return jsonify(place.to_dict())
        except KeyError:
            abort(404)

    # DELETE REQUESTS
    elif request.method == 'DELETE':
        places = storage.all(Place)
        try:
            key = 'Place.' + place_id
            storage.delete(places[key])
            storage.save()
            return jsonify({}), 200
        except KeyError:
            abort(404)

    # PUT REQUESTS
    elif request.method == 'PUT':
        places = storage.all(Place)
        key = 'Place.' + place_id
        try:
            place = places[key]

            if request.is_json:
                body_request = request.get_json()
            else:
                abort(400, 'Not a JSON')

            ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
            for key, val in body_request.items():
                if key not in ignore:
                    setattr(place, key, val)

            storage.save()
            return jsonify(place.to_dict()), 200

        except KeyError:
            abort(404)

    # UNSUPPORTED REQUESTS
    else:
        abort(501)

