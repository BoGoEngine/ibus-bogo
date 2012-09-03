#
# IBus-Bogo - The Vietnamese IME for IBus
#
# Copyright (c) 2012- Long T. Dam <longdt90@gmail.com>,
#                     Trung Ngo <ndtrung4419@gmail.com>
#
# This file is part of IBus-BoGo Project
# IBus-Bogo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# IBus-BoGo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with IBus-BoGo.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import GObject
from gi.repository import IBus
from gi.repository import Pango
import BoGo

# syntactic sugar
keysyms = IBus
modifier = IBus.ModifierType

import time
from ctypes import *

Xtst = CDLL("libXtst.so.6")
Xlib = CDLL("libX11.so.6")
dpy = Xtst.XOpenDisplay(None)
sym = Xlib.XStringToKeysym("BackSpace")
bg_backspace = Xlib.XKeysymToKeycode(dpy, sym)
time_delay = 0.006

class Engine(IBus.Engine):
    __gtype_name__ = 'EngineBoGo'

    def __init__(self):
        super(Engine, self).__init__()
        self.reset_engine()
        print "Finish Initialization. Time delay: ", time_delay


    # The "do_" part is PyGObject's way of overriding base's functions
    def do_process_key_event(self, keyval, keycode, state):
               # ignore key release events
        time.sleep(time_delay)
        is_press = ((state & modifier.RELEASE_MASK) == 0)
        if not is_press:
            return False

        if self.is_character(keyval):
            if state & (modifier.CONTROL_MASK | modifier.MOD1_MASK) == 0:
                print "Character entered: " + chr(keyval)
                self.isFakeBackspace = True

                self.old_string = self.new_string
                self.process_key(keyval)
                print "Old string:", self.old_string
                print "New string:", self.new_string
                self.n_backspace, self.string_to_commit = \
                  self.get_nbackspace_and_string_to_commit()
                print "n_backspace: ", self.n_backspace
                print "String to commit:", self.string_to_commit
                self.commit_fake_backspace()
                return True

        if self.string_to_commit:
            if keyval == keysyms.Return or keyval == keysyms.Escape or\
               keyval == keysyms.space:
                self.reset_engine()
                return False

            if keyval == keysyms.BackSpace:
                if self.isFakeBackspace:
                    print "Fake backspace no. " + str(self.n_backspace)
                    self.n_backspace -= 1
                    if self.n_backspace == 0:
                        print "Last fake backspace. Commit..."
                        self.commit_result()
                        self.isFakeBackspace = False
                        return True
                else:
                    print "A real backspace"
                    self.remove_last_char()
                return False

        self.reset_engine()
        return False

    def reset_engine(self):
        self.string_to_commit = u""
        self.new_string = u""
        self.old_string = u""
        self.isFakeBackspace = False
        self.n_backspace = 0

    def commit_result(self):
        self.commit_text(IBus.Text.new_from_string(self.string_to_commit))

    def process_key(self, keyval):
        #self.new_string += unichr(keyval)
        ukeyval = unichr(keyval)
        if self.old_string:
            print BoGo.process_key(self.old_string, ukeyval)
            self.new_string = BoGo.process_key(self.old_string, ukeyval)
        else:
            self.new_string = ukeyval

    def remove_last_char(self):
        self.new_string = self.new_string[:-1]

    def commit_fake_backspace(self):
        global dpy, bg_backspace
        print "Commit "+ str(self.n_backspace) + " fake Backspaces"
        number = self.n_backspace #Silly Python
        for i in range(number):
            Xtst.XTestFakeKeyEvent(dpy, bg_backspace, True, 0)
            Xtst.XTestFakeKeyEvent(dpy, bg_backspace, False, 0)
            Xlib.XFlush(dpy)

    def get_nbackspace_and_string_to_commit(self):
        if (self.old_string):
            length = len(self.old_string)
            for i in range(length):
                if self.old_string[i] != self.new_string[i]:
                    _nbackspace = length - i + 1
                    _stringtocommit = self.new_string[i:]
                    return _nbackspace, _stringtocommit
            return 1, self.new_string[length:]
        else:
             return 1, self.new_string
        # Classical method:
        # return len(self.old_string) + 1, self.new_string

    def is_character(self, keyval):
        if keyval in xrange(33,126):
            return True
        else:
            return False

    def is_ending_character(self, keyval):
        pass
