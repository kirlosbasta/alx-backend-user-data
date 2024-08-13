#!/usr/bin/env python3
'''User Authentication module'''
import bcrypt


def _hash_password(password: str) -> bytes:
    '''Hash a string and return the hashed bytes'''
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
