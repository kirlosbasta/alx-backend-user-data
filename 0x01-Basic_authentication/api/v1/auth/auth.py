#!/usr/bin/env python3
'''
3.Auth class
'''
from flask import request
from typing import List, TypeVar


class Auth():
    '''
    Authentiaction class
    '''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''pass to later'''
        if path is None or not excluded_paths:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        '''pass to later'''
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        '''pass to later'''
