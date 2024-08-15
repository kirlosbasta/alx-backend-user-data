#!/usr/bin/env python3
'''Integration test for flask app endpoints'''
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
URL = 'http://0.0.0.0:5000'


def register_user(email: str, password: str) -> None:
    '''Test POST /users route'''
    FORM_DATA = {'email': email, 'password': password}
    response = requests.post(URL + '/users', data=FORM_DATA)
    assert response.status_code == 200
    assert response.json() == {"email": EMAIL, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    '''Login using wrong password'''
    FORM_DATA = {'email': email, 'password': password}
    response = requests.post(URL + '/sessions', data=FORM_DATA)
    assert response.status_code == 401


def profile_unlogged() -> None:
    '''requset profile without logging in '''
    response = requests.get(URL + '/profile')
    assert response.status_code == 403


def log_in(email: str, password: str) -> str:
    '''Login a user'''
    FORM_DATA = {'email': email, 'password': password}
    response = requests.post(URL + '/sessions', data=FORM_DATA)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get('session_id')


def profile_logged(session_id: str) -> None:
    '''TEST GET /profile route logged in'''
    response = requests.get(URL + '/profile',
                            cookies={'session_id': session_id})
    assert response.status_code == 200
    assert response.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    '''TEST logout mechanisme'''
    response = requests.delete(URL + '/sessions',
                               cookies={'session_id': session_id},
                               allow_redirects=True)
    assert response.status_code == 200
    # When session is deleted it redirects to GET /
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    '''TEST POST /reset_password route'''
    FORM_DATA = {'email': email}
    response = requests.post(URL + '/reset_password', data=FORM_DATA)
    assert response.status_code == 200
    json = response.json()
    assert json.get('email') == email
    return json.get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    '''Test update password mechanism'''
    FORM_DATA = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
        }
    response = requests.put(URL + '/reset_password', data=FORM_DATA)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
