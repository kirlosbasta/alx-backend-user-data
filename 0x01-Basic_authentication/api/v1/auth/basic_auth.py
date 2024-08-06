#!/usr/bin/env python3
'''
6.BasicAuth class
'''
from api.v1.auth.auth import Auth
from flask import request
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    '''Implement Basic Authentication'''
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        '''return authorization details from the header'''
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self, header: str) -> str:
        '''decode base64 authorization header to a utf-8 string'''
        if header is None:
            return None
        if not isinstance(header, str):
            return None
        try:
            return (base64.b64decode(s=header, validate=True)).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 base64_header: str) -> (str, str):
        '''
        separate username and password from decoded_base64_authorization_header
        '''
        if base64_header is None:
            return None, None
        if not isinstance(base64_header, str):
            return None, None
        if ':' not in base64_header:
            return None, None
        username, password = base64_header.split(':', maxsplit=1)
        return username, password

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        '''return user object if found and user_pwd matches'''
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        users = User.search({'email': user_email})
        if len(users) <= 0:
            return None
        user = users[0]
        if not isinstance(user, User):
            return None
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        '''return the user if exists otherwise None'''
        authorization = self.authorization_header(request)
        if authorization is None:
            return None
        authorization_data = self.\
            extract_base64_authorization_header(authorization)
        if authorization_data is None:
            return None
        authorization_data_decoded = self.\
            decode_base64_authorization_header(authorization_data)
        if authorization_data_decoded is None:
            return None
        email, password = self.\
            extract_user_credentials(authorization_data_decoded)
        if email is None or password is None:
            return None
        user = self.user_object_from_credentials(email, password)
        if user is None:
            return None
        return user
