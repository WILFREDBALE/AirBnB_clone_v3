#!/usr/bin/python3
"""
This module contains the view for State objects
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State

objects = storage.all(State)


@app_views.route('/states', strict_slashes=False)
def states():
    """retrieves the list of all State objects"""
    obj_list = [obj.to_dict() for obj in objects.values()]
    return jsonify(obj_list)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """retrieves a State object using it's id"""
    obj = objects.get('State.' + state_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    """deletes a State object"""
    obj = objects.get('State.' + state_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    return jsonify({})
