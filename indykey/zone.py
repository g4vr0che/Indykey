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
"""

import dbus

bus = dbus.SystemBus()
remote_object = bus.get_object('com.github.g4vr0che.indykey', 'IndykeyObject')

class Zone:
    def __init__(self, path):
        self.path = path

    @property
    def color(self):
        """str: The color value of this zone as stored in the driver."""
        with open(self.path) as zone_file:
            color = zone_file.readline().strip()
            
        return color
    
    @color.setter
    def color(self, color):
        """We talk to our dbus object to set the color using polkit."""
        remote_object.SetColor(self.path, color)
