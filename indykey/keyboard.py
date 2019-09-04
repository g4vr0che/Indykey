#!/usr/bin/python3

"""
 Indykey
 A library for controlling keyboard backlight brightness

 Copyright 2017-2018 Ian Santopietro <isantop@gmail.com>

Permission to use, copy, modify, and/or distribute this software for any purpose
with or without fee is hereby granted, provided that the above copyright notice
and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
THIS SOFTWARE.

 This is a keyboard library. Is represents transforming colors from Indykey to
 the values supported by the keyboard.
"""

from enum import Enum
import os

SYSTEM76_CONFIG = {
    'type': 'rgb',
    'brightness': True,
    'zones': 3,
    'format': 'hex@RRGGBB'
}

class KeyboardError(Exception):
    """An error from the Keyboard.

    Arguments: 
        msg (str): message describing the error
        code (:obj:`int`, optional, default=1): Exception error code.
    """
    def __init__(self, msg, code=1):
        self.msg = msg
        self.code = code

class typ(Enum):
    RGB = (1, 'rgb')
    LIST = (2, 'list')
    NOCOLOR = (3, 'nocolor')
    ONECOLOR = (4, 'onecolor')


class Keyboard:
    def __init__(self, path='/dev/null'):

        self._store = {}

    @property
    def kind(self):
        try:
            return self._store['kind']
        except KeyError:
            return None
    
    @kind.setter
    def kind(self, kb_kind):
        try:
            self._store['kind'] = typ[kb_kind.upper()]
        except KeyError:
            valid_types = ""
            for t in typ:
                valid_types += f'{t.value[1]}\n'
            raise KeyboardError(
                f'We got the wrong type of error. Valid types are:\n'
                f'{valid_types}'
            )
    
    @property
    def brightness(self):
        try:
            return self._store['brightness']
        except KeyError:
            return True
        
    @brightness.setter
    def brightness(self, bright):
        if isinstance(bright, bool):
            self._store['brightness'] = bright
        else:
            raise KeyboardError(
                'Keyboard brightness value must be a boolean value.'
            )