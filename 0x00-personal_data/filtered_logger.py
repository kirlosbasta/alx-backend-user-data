#!/usr/bin/env python3
'''0. Regex-ing'''
import re
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
