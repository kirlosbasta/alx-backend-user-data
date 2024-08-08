#!/usr/bin/env python3
'''
Session DB Authentication system
'''
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    '''Inherent from SessionExpAuth and store session in a file'''

    def create_session(self, user_id=None):
        '''create a Session and store it in a file'''
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(**{'session_id': session_id,
                                      'user_id': user_id})
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''return user_id from session_id'''
        UserSession.load_from_file()
        if session_id is None:
            return None
        user_sessions = UserSession.search({'session_id': session_id})
        if len(user_sessions) == 0:
            return None
        user_session = user_sessions[0]
        created_at = user_session.created_at
        if created_at is None:
            return None
        timeframe = created_at + timedelta(seconds=self.session_duration)
        if timeframe < datetime.now():
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        '''Delete UserSession'''
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        user_sessions = UserSession.search({'session_id': session_id})
        if len(user_sessions) == 0:
            return False
        user_session = user_sessions[0]
        user_session.remove()
        return True
