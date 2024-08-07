#!/usr/bin/env python3
'''5. Encrypting passwords'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''Hash a pasword using bcrypt'''
    return bcrypt.hashpw(bytes(password, encoding='utf-8'),
                         salt=bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''check if password matches the hashed password'''
    return bcrypt.checkpw(bytes(password, encoding='utf-8'), hashed_password)
