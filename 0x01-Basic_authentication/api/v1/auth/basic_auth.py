#!/usr/bin/env python3
'''
6.BasicAuth class
'''
from api.v1.auth.auth import Auth
from flask import request
import base64


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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                            )-> str:
        '''decode base64 authorization header to a utf-8 string'''
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            return (base64.b64decode(s=base64_authorization_header, validate=True)).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        '''separate username and password from decoded_base64_authorization_header'''
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        username, password = decoded_base64_authorization_header.split(':', maxsplit=1)
        return username, password
