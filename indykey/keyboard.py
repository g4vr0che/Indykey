#!/usr/bin/python3

"""
 Indykey
 A library for controlling keyboard backlight brightness

 Copyright 2019 Gaven Royer <gavroyer@gmail.com>

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

import dbus
import os

from . import zone

bus = dbus.SystemBus()
remote_object = bus.get_object('com.github.g4vr0che.indykey', '/IndykeyObject')

class KeyboardException(Exception):
    """Exception when something goes wrong with the keyboard

    Arguments: 
        msg (str): Human-readable message describing the error that threw the 
            exception.
        code (:obj:`int`, optional, default=1): Exception error code.
    """
    def __init__(self, msg, code=1):
        self.msg = msg
        self.code = code

class Keyboard:
    def __init__(self, path):
        self.path = path
        self.brt_path = os.path.join(self.path, 'brightness')
        self.mb_path = os.path.join(self.path, 'max_brightness')
    
    @property
    def max_brightness(self):
        """int: The highest the brightness will go."""
        with open(self.mb_path) as mb_file:
            mb = int(mb_file.read())
        
        return mb
    
    @property
    def raw_brightness(self):
        """int: the raw value of the brightness."""
        with open(self.brt_path) as brt_file:
            rb = int(brt_file.read())
        return rb
    
    @raw_brightness.setter
    def raw_brightness(self, brt):
        """Set the brightness to the file after checking the value.
        """
        if brt >= 0 and brt <= self.max_brightness:
            remote_object.SetBrightness(self.brt_path, int(brt))
        elif brt < 0:
            remote_object.SetBrightness(self.brt_path, 0)
        elif brt > self.max_brightness:
            remote_object.SetBrightness(self.brt_path, self.max_brightness)
    
    @property
    def brightness(self):
        """float: A percentage from 1 to 100 indicating the current brightness.
        """
        with open(self.brt_path) as brt_file:
            raw_brightness = int(brt_file.read())
        return round(raw_brightness / self.max_brightness * 100)

    @brightness.setter
    def brightness(self, brt):
        """This just converts the value to the correct int value and sets
        self.raw_brightness instead.
        """
        rb = brt / 100 * self.max_brightness
        self.raw_brightness = int(rb)
