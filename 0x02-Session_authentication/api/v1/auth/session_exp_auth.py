#!/usr/bin/env python3
'''class SessionExpAuth that inherits from SessionAuth'''
from api.v1.auth.session_auth import SessionAuth
import datetime
from os import getenv


class SessionExpAuth(SessionAuth):
    '''Manages the expiration of a session'''
    def __init__(self):
        '''initialize expiration data'''
        duration = getenv('SESSION_DURATION', 0)
        try:
            self.session_duration = int(duration)
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        '''create a session'''
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''
        return user_id only if the expiration date is still valid or
        the session is permenant
        '''
        if session_id is None:
            return None
        session_obj = self.user_id_by_session_id.get(session_id)
        if session_obj is None:
            return None
        if self.session_duration <= 0:
            return session_obj.user_id
        created_at = session_obj.get('created_at')
        if created_at is None:
            return None
        if created_at + datetime.timedelta(seconds=self.session_duration) <\
                datetime.datetime.now():
            return None
        return session_obj.get('user_id')
