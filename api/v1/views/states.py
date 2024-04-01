#!/usr/bin/python3
"""
for states API
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def states(state_id=None):
    """Handles HTTP requests for State objects"""
    if request.method == 'GET':
        if state_id:
            state = storage.get(State, state_id)
            if state:
                return jsonify(state.to_dict())
            else:
                abort(404)
        else:
            states = storage.all(State).values()
            return jsonify([state.to_dict() for state in states])

    elif request.method == 'DELETE':
        state = storage.get(State, state_id)
        if state:
            storage.delete(state)
            storage.save()
            return jsonify({}), 200
        else:
            abort(404)

    elif request.method == 'POST':
        if not request.json:
            return jsonify({"error": "Not a JSON"}), 400
        if 'name' not in request.json:
            return jsonify({"error": "Missing name"}), 400
        data = request.json
        new_state = State(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201

    elif request.method == 'PUT':
        state = storage.get(State, state_id)
        if state:
            data = request.json
            if not data:
                return jsonify({"error": "Not a JSON"}), 400
            for key, value in data.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(state, key, value)
            state.save()
            return jsonify(state.to_dict()), 200
        else:
            abort(404)

    else:
        abort(501)
