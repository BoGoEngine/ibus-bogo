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
BG_BACKSPACE = Xlib.XKeysymToKeycode(dpy, sym)
CharacterLimit = 8

class Engine(IBus.Engine):
    __gtype_name__ = 'EngineBoGo'

    def __init__(self):
        super(Engine, self).__init__()
        self.reset_engine()
        print "Finish Initialization"


    # The "do_" part is PyGObject's way of overriding base's functions
    def do_process_key_event(self, keyval, keycode, state):
               # ignore key release events
        time.sleep(0.002)
        is_press = ((state & modifier.RELEASE_MASK) == 0)
        if not is_press:
            return False

        if self.is_character(keyval):
            if state & (modifier.CONTROL_MASK | modifier.MOD1_MASK) == 0:
                print "Character entered: " + chr(keyval)
                self.isFakeBackspace = True

                self.OldString = self.NewString
                self.process_key(keyval)
                print "Old string:", self.OldString
                print "New string:", self.NewString
                self.nBackspace, self.StringToCommit = \
                  self.get_nbackspace_and_string_to_commit()
                print "nBackspace: ", self.nBackspace
                print "String to commit:", self.StringToCommit
                self.commit_fake_backspace()
                return True

        if self.StringToCommit:
            if keyval == keysyms.Return or keyval == keysyms.Escape or\
               keyval == keysyms.space:
                self.reset_engine()
                return False

            if keyval == keysyms.BackSpace:
                if self.isFakeBackspace:
                    print "Fake backspace no. " + str(self.nBackspace)
                    self.nBackspace -= 1
                    if self.nBackspace == 0:
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
        self.StringToCommit = u""
        self.NewString = u""
        self.OldString = u""
        self.isFakeBackspace = False
        self.nBackspace = 0

    def commit_result(self):
        self.commit_text(IBus.Text.new_from_string(self.StringToCommit))

    def process_key(self, keyval):
        #self.NewString += unichr(keyval)
        ukeyval = unichr(keyval)
        if self.OldString:
            print BoGo.process_key(self.OldString, ukeyval)
            self.NewString = BoGo.process_key(self.OldString, ukeyval)
        else:
            self.NewString = ukeyval

    def remove_last_char(self):
        self.NewString = self.NewString[:-1]

    def commit_fake_backspace(self):
        global dpy, BG_BACKSPACE
        print "Commit "+ str(self.nBackspace) + " fake Backspaces"
        number = self.nBackspace #Silly Python
        for i in range(number):
            Xtst.XTestFakeKeyEvent(dpy, BG_BACKSPACE, True, 0)
            Xtst.XTestFakeKeyEvent(dpy, BG_BACKSPACE, False, 0)
            Xlib.XFlush(dpy)

    def get_nbackspace_and_string_to_commit(self):
        if (self.OldString):
            length = len(self.OldString)
            for i in range(length):
                if self.OldString[i] != self.NewString[i]:
                    _nbackspace = length - i + 1
                    _stringtocommit = self.NewString[i:]
                    return _nbackspace, _stringtocommit
            return 1, self.NewString[length:]
        else:
             return 1, self.NewString
        # Classical method:
        # return len(self.OldString) + 1, self.NewString

    def is_character(self, keyval):
        if keyval in xrange(33,126):
            return True
        else:
            return False

    def is_ending_character(self, keyval):
        pass
