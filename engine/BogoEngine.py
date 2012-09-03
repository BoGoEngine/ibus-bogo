# IBus-Bogo - The Vietnamese IME for IBus
#
# Copyright (c) 2012- Long T. Dam <longdt90@gmail.com>,
#                     Trung Ngo <ndtrung4419@gmail.com>
#
# This file is part of IBus-Bogo Project
# IBus-Bogo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# IBus-Bogo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with IBus-Bogo.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import GObject
from gi.repository import IBus
from gi.repository import Pango

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
        self.resetEngine()
        print "Finish Initialization"


    # The "do_" part is PyGObject's way of overriding base's functions
    def do_process_key_event(self, keyval, keycode, state):
               # ignore key release events
        time.sleep(0.002)
        is_press = ((state & modifier.RELEASE_MASK) == 0)
        if not is_press:
            return False

        if self.isCharacter(keyval):
            if state & (modifier.CONTROL_MASK | modifier.MOD1_MASK) == 0:
                print "Character entered: " + chr(keyval)
                self.isFakeBackspace = True

                #Optimization
                # if (self.nBackspace == CharacterLimit):
                #     self.resetEngine()
                #     self.StringToCommit = unichr(keyval)
                #     self.commitPreedit()
                #     return True
                self.OldString = self.NewString
                self.processChar(keyval)
                print "Old string:", self.OldString
                print "New string:", self.NewString
                self.nBackspace, self.StringToCommit = \
                  self.getFakeBackspace_StringToCommit()
                print "String to commit:", self.StringToCommit
                self.commitFakeBackspace()
                return True

        if self.StringToCommit:
            if keyval == keysyms.Return or keyval == keysyms.Escape or\
               keyval == keysyms.space:
                self.resetEngine()
                return False

            if keyval == keysyms.BackSpace:
                if self.isFakeBackspace:
                    print "Fake backspace no. " + str(self.nBackspace)
                    self.nBackspace -= 1
                    if self.nBackspace == 0:
                        print "Last fake backspace. Commit..."
                        self.commitResult()
                        self.isFakeBackspace = False
                        return True
                else:
                    print "A real backspace"
                    self.removeLastChar()
                return False

        self.resetEngine()
        return False

    def resetEngine(self):
        self.StringToCommit = u""
        self.NewString = u""
        self.OldString = u""
        self.isFakeBackspace = False
        self.nBackspace = 0

    def commitResult(self):
        self.commit_text(IBus.Text.new_from_string(self.StringToCommit))

    def processChar(self, char):
        self.NewString += unichr(char)

    def removeLastChar(self):
        self.NewString = self.NewString[:-1]

    def commitFakeBackspace(self):
        global dpy, BG_BACKSPACE
        print "Commit "+ str(self.nBackspace) + " fake Backspaces"
        number = self.nBackspace #Silly Python
        for i in range(number):
            Xtst.XTestFakeKeyEvent(dpy, BG_BACKSPACE, True, 0)
            Xtst.XTestFakeKeyEvent(dpy, BG_BACKSPACE, False, 0)
            Xlib.XFlush(dpy)

    def getFakeBackspace_StringToCommit(self):
        length = len(self.OldString)
        if length == 0:
            return 1, self.NewString
        for i in range(length):
            if self.OldString[i] != self.NewString[i]:
                _nbackspace = length - i + 1
                _stringtocommit = self.NewString[i + 1:]
                return _nbackspace, _stringtocommit
        return 1, self.NewString[length:]

    def isCharacter(self, keyval):
        if keyval in xrange(33,126):
            return True
        else:
            return False

    def isEndingCharacter(self, keyval):
        pass
