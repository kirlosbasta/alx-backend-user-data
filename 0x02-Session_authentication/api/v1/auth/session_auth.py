#!/usr/bin/env python3
'''
class SessionAuth that inherits from Auth
'''
from api.v1.auth.auth import Auth
from flask import request
import base64
from typing import TypeVar, Dict
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    '''Session base authentication class'''
    user_id_by_session_id: Dict = {}

    def create_session(self, user_id: str = None) -> str:
        '''Create Session ID for user_id'''
        if type(user_id) is not str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''return user_id from session id'''
        if type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        '''return User instance based on cookie value'''
        cookie_session_id = self.session_cookie(request)
        if cookie_session_id is None:
            return None
        user_id = self.user_id_for_session_id(cookie_session_id)
        if user_id is None:
            return None
        return User.get(user_id)
