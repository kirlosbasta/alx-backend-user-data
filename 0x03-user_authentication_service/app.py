#!/usr/bin/env python3
'''App Dirver Module'''
from flask import (Flask, jsonify, request, abort,
                   make_response, url_for, redirect)
from auth import Auth


app = Flask(__name__)
app.url_map.strict_slashes = False
AUTH = Auth()


@app.route('/', methods=['GET'])
def bienvenue() -> str:
    '''return a simple message'''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    '''Regestir a user'''
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    '''Manages login'''
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    res = make_response(jsonify({"email": email, "message": "logged in"}))
    res.set_cookie("session_id", session_id)
    return res


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    '''Logout a user'''
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user_id=user.id)
    return redirect(url_for('bienvenue'))


@app.route('/profile', methods=['GET'])
def profile() -> str:
    '''Return info about the user if exists'''
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    '''genrate a reset_token for the user'''
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email=email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": token})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
