#!/usr/bin/python3
"""
City API view
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def cities_get(state_id=None, city_id=None):
    """Manage all methods on cities"""
    if request.method == 'GET':
        if state_id:
            # Retrieve all cities of a specific state
            state = storage.get('State', state_id)
            if state is None:
                abort(404)
            cities = storage.all('City')
            return jsonify([city.to_dict() for city in cities.values()
                            if city.state_id == state_id])
        else:
            # Retrieve a specific city
            city = storage.get('City', city_id)
            if city is None:
                abort(404)
            return jsonify(city.to_dict())

    elif request.method == 'DELETE':
        city = storage.get('City', city_id)
        if city is None:
            abort(404)
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

    elif request.method == 'POST':
        if not request.is_json:
            abort(400, 'Not a JSON')
        body_request = request.get_json()
        if 'name' not in body_request or 'state_id' not in body_request:
            abort(400, 'Missing name or state_id')
        new_city = City(**body_request)
        storage.new(new_city)
        storage.save()
        return jsonify(new_city.to_dict()), 201

    elif request.method == 'PUT':
        city = storage.get('City', city_id)
        if city is None:
            abort(404)
        if not request.is_json:
            abort(400, 'Not a JSON')
        body_request = request.get_json()
        for key, val in body_request.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, val)
        storage.save()
        return jsonify(city.to_dict()), 200

    else:
        abort(501)
