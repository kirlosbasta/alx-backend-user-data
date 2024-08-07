#!/usr/bin/env python3
'''0. Regex-ing'''
import re
import logging
from os import environ
from mysql.connector import connection
from typing import List


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    '''return the message with all the fields obfuscated by redaction'''
    message_data = message.split(separator)
    for i in range(len(fields)):
        message_data = [re.sub(rf'{fields[i]}=.+',
                               f'{fields[i]}={redaction}',
                               data) for data in message_data]
    return separator.join(message_data)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Constructor method
            """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Format method
            """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    '''return a logging.Logger object'''
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream = logging.StreamHandler()
    stream.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream)
    return logger


def get_db() -> connection.MySQLConnection:
    """
    Connect to mysql server with environmental vars
    """
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME", 'my_db')
    connector = connection.MySQLConnection(
        user=username,
        password=password,
        host=db_host,
        database=db_name)
    return connector


def main() -> None:
    '''Driver function'''
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()
    for row in cursor:
        logger.info('name={}; email={}; phone={}; ssn={}; password={};\
                    ip={}; last_login={}; user_agent={};'.format(
            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
