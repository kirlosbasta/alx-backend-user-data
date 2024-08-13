#!/usr/bin/env python3
'''User Authentication module'''
import bcrypt
from db import DB
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    '''Hash a string and return the hashed bytes'''
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    '''return random uuid'''
    return uuid4()


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''
        create and return the user if not exist otherwise
        raise ValueError
        '''
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            user = self._db.add_user(email=email, hashed_password=hashed_pwd)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        '''validate if the user exist and the password is matching'''
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)
