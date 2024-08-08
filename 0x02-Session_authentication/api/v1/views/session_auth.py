#!/usr/bin/env python3
'''view for Session Authentication'''
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    '''login the user to the session'''
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': email})
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    resp = make_response(jsonify(user.to_json()))
    resp.set_cookie(getenv('SESSION_NAME'), session_id)
    return resp


@app_views.route('auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> str:
    '''Logout from current session'''
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
