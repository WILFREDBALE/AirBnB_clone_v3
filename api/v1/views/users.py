#!/usr/bin/python3
"""This module contains the view for User objects"""
from flask import abort, jsonify, request, current_app
from models.user import User
from models import storage
from api.v1.views import app_views
from datetime import datetime

objects = storage.all(User)
clskeyprefix = 'User.'

@app_views.route('/users', strict_slashes=False)
def users():
    """retrieves the list of all User objects"""
    return jsonify([obj.to_dict() for obj in objects.values()])


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user_by_id(user_id):
    """retrieves a User object using it's id"""
    user = objects.get(clskeyprefix + user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user_by_id(user_id):
    """deletes a User object"""
    obj = objects.get(clskeyprefix + user_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """creates a User object"""
    if not request.json:
        abort(400, 'Not a JSON')
    if 'email' not in request.json:
        abort(400, 'Missing email')
    if 'password' not in request.json:
        abort(400, 'Missing password')
    obj = User(**request.json)
    with current_app.app_context():
        storage.new(obj)
        storage.save()
    return jsonify(obj.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """updates a User object"""
    obj = objects.get(clskeyprefix + user_id)
    if not obj:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for key, value in request.json.items():
        if (key in obj.__dict__ and key not in
        ['id', 'email', 'created_at', 'updated_at']):
            setattr(obj, key, value)
    setattr(obj, 'updated_at', datetime.utcnow())
    storage.save()
    return jsonify(obj.to_dict()), 200
