#!/usr/bin/env python3
'''
3.Auth class
'''
from flask import request
from typing import List, TypeVar
import re


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
        for excluded_path in excluded_paths:
            if re.search(excluded_path, path) is not None:
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
