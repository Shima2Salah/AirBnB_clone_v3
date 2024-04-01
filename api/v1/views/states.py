#!/usr/bin/python3
"""
State Api view
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def states_get(state_id=None):
    """to manage all methods on states"""
    if request.method == 'GET':
        if not state_id:
            states = storage.all(State)
            return jsonify([st.to_dict() for st in states.values()])
        else:
            state = storage.get(State, state_id)
            if state is None:
                abort(404)
            return jsonify(state.to_dict())

    elif request.method == 'DELETE':
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        storage.delete(state)
        storage.save()
        return jsonify({}), 200

    elif request.method == 'POST':
        if not request.is_json:
            abort(400, 'Not a JSON')
        body_request = request.get_json()
        if 'name' not in body_request:
            abort(400, 'Missing name')
        new_state = State(**body_request)
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201

    elif request.method == 'PUT':
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        if not request.is_json:
            abort(400, 'Not a JSON')
        body_request = request.get_json()
        for key, val in body_request.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, val)
        storage.save()
        return jsonify(state.to_dict()), 200

    else:
        abort(501)
