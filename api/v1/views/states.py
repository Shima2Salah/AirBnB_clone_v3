#!/usr/bin/python3
"""
for states API
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ To get all states """
    states = storage.all("State")
    res = []
    for st in states.values():
        res.append(st.to_dict())
    return jsonify(res)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def getstate(state_id=None):
    """Retrieves a State object """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def deletestate(state_id=None):
    """Delete a state by id"""
    state = storage.get("State", str(state_id))
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_state():
    """create a new state"""
    val = request.json
    if not val:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in val:
        return jsonify({"error": "Missing name"}), 400
    new_state = State(**val)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    """change state data by id"""
    ans = storage.get("State", str(state_id))
    if ans is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    for key, val in request.json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(ans, key, val)
    ans.save()
    return jsonify(ans.to_dict()), 200
