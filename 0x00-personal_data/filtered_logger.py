#!/usr/bin/env python3
'''0. Regex-ing'''
import re
import logging
from typing import List


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

