#!/usr/bin/env python3
'''App Dirver Module'''
from flask import Flask, jsonify, request, abort, make_response
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
