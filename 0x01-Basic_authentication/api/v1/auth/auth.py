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
        return False
    
    def authorization_header(self, request=None) -> str:
        '''pass to later'''
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        '''pass to later'''
