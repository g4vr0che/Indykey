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
    

class kind(Enum):
    RGB = (1, 'rgb')
    LIST = (2, 'list')
    NOCOLOR = (3, 'nocolor')



class Keyboard:
    def __init__(self, path='/dev/null'):

        self.kind = kind.RGB
        self.brightness = True
        self.zones = 3
        self.format: 'hex@RRGGBB'
        self._store = {}

    @property
    def kind(self):
        try:
            return self._store['type']
        except KeyError:
            return None
    
    @kind.setter
    def kind(self, kb_kind)
        try:
            self._store['kind'] = kind[kb_kind]
        except KeyError:
