#!/usr/bin/env python3
'''
3.Auth class
'''
from flask import request
from typing import List, TypeVar
import re
from os import getenv


class Auth():
    '''
    Authentiaction class
    '''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''pass to later'''
        if path is None or not excluded_paths:
            return True
        for excluded_path in excluded_paths:
            pattern = ''
            if excluded_path[-1] == '*':
                pattern = '{}.*'.format(excluded_path[0:-1])
            else:
                pattern = excluded_path[:-1]
            if re.search(pattern, path) is not None:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        '''pass to later'''
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        '''pass to later'''
        pass

    def session_cookie(self, request=None):
        '''return cookie value from request'''
        if request is None:
            return None
        cookie_name = getenv('SESSION_NAME')
        return request.cookies.get(cookie_name)
