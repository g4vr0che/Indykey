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
import gi
from gi.repository import GObject

import dbus
import dbus.service
import dbus.mainloop.glib
import time

class IndykeyException(dbus.DBusException):
    _dbus_error_name = 'com.github.g4vr0che.indykey.IndykeyException'

class PermissionDeniedByPolicy(dbus.DBusException):
    _dbus_error_name = 'com.github.g4vr0che.indykey.PermissionDeniedByPolicy'

class ColorException(Exception):
    """Exception when a color couldn't be set

    Arguments: 
        msg (str): Human-readable message describing the error that threw the 
            exception.
        code (:obj:`int`, optional, default=1): Exception error code.
    """
    def __init__(self, msg, code=1):
        self.msg = msg
        self.code = code

class IndykeyObject(dbus.service.Object):

    def __init__(self, conn=None, object_path=None, bus_name=None):
        dbus.service.Object.__init__(self, conn, object_path, bus_name)

        # Used by _check_polkit_privilige
        self.dbus_info = None
        self.polkit = None
        self.enforce_polkit = True

    @dbus.service.method(
        'com.github.g4vr0che.Interface',
        in_signature='ss', out_signature='i',
        sender_keyword='sender', connection_keyword='conn'
    )
    def SetColor(self, zone_path, color, sender=None, conn=None):
        self._check_polkit_privilege(
            sender, conn, 'com.github.g4vr0che.indykey.setcolor'
        )
        try:
            with open(zone_path, mode='w') as zone_file:
                zone_file.write(color)
        except FileNotFoundError:
            raise
        return 0
    
    @classmethod
    def _log_in_file(klass, filename, string):
        date = time.asctime(time.localtime())
        ff = open(filename, "a")
        ff.write("%s : %s\n" %(date,str(string)))
        ff.close()
    
    @classmethod
    def _strip_source_line(self, source):
        source = source.replace("#", "# ")
        source = source.replace("[", "")
        source = source.replace("]", "")
        source = source.replace("'", "")
        source = source.replace("  ", " ")
        return source

    def _check_polkit_privilege(self, sender, conn, privilege):
        '''Verify that sender has a given PolicyKit privilege.

        sender is the sender's (private) D-BUS name, such as ":1:42"
        (sender_keyword in @dbus.service.methods). conn is
        the dbus.Connection object (connection_keyword in
        @dbus.service.methods). privilege is the PolicyKit privilege string.

        This method returns if the caller is privileged, and otherwise throws a
        PermissionDeniedByPolicy exception.
        '''
        if sender is None and conn is None:
            # called locally, not through D-BUS
            return
        if not self.enforce_polkit:
            # that happens for testing purposes when running on the session
            # bus, and it does not make sense to restrict operations here
            return

        # get peer PID
        if self.dbus_info is None:
            self.dbus_info = dbus.Interface(conn.get_object('org.freedesktop.DBus',
                '/org/freedesktop/DBus/Bus', False), 'org.freedesktop.DBus')
        pid = self.dbus_info.GetConnectionUnixProcessID(sender)
        
        # query PolicyKit
        if self.polkit is None:
            self.polkit = dbus.Interface(dbus.SystemBus().get_object(
                'org.freedesktop.PolicyKit1',
                '/org/freedesktop/PolicyKit1/Authority', False),
                'org.freedesktop.PolicyKit1.Authority')
        try:
            # we don't need is_challenge return here, since we call with AllowUserInteraction
            (is_auth, _, details) = self.polkit.CheckAuthorization(
                    ('unix-process', {'pid': dbus.UInt32(pid, variant_level=1),
                    'start-time': dbus.UInt64(0, variant_level=1)}), 
                    privilege, {'': ''}, dbus.UInt32(1), '', timeout=600)
        except dbus.DBusException as e:
            if e._dbus_error_name == 'org.freedesktop.DBus.Error.ServiceUnknown':
                # polkitd timed out, connect again
                self.polkit = None
                return self._check_polkit_privilege(sender, conn, privilege)
            else:
                raise

        if not is_auth:
            IndykeyObject._log_in_file('/tmp/indykey.log','_check_polkit_privilege: sender %s on connection %s pid %i is not authorized for %s: %s' %
                    (sender, conn, pid, privilege, str(details)))
            raise PermissionDeniedByPolicy(privilege)


if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()
    name = dbus.service.BusName("com.github.g4vr0che.indykey", bus)
    object = IndykeyObject(bus, '/IndykeyObject')

    mainloop = GObject.MainLoop()
    mainloop.run()
