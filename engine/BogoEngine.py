# IBus-Bogo - The Vietnamese IME for IBus
#
# Copyright (c) 2012 Dam Tien Long <longdt90@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import gobject
import pango
import ibus
from ibus import keysyms
from ibus import modifier
import time
from ctypes import *

Xtst = CDLL("libXtst.so.6")
Xlib = CDLL("libX11.so.6")
dpy = Xtst.XOpenDisplay(None)
BG_BACKSPACE = 22
CharacterLimit = 8

class Engine(ibus.EngineBase):

    def __init__(self, bus, object_path):
        super(Engine, self).__init__(bus, object_path)
        self.__preedit_string = u""
        self.nBackspace = 0
        self.isFakeBackspace = False;
        print "Finish Initialization"


    def process_key_event(self, keyval, keycode, state):
               # ignore key release events
        time.sleep(0.0016)
        is_press = ((state & modifier.RELEASE_MASK) == 0)
        if not is_press:
            return False

        if self.isCharacter(keyval):
            if state & (modifier.CONTROL_MASK | modifier.ALT_MASK) == 0:
                print "Character entered: " + chr(keyval)
                self.isFakeBackspace = True
                self.nBackspace = len(self.__preedit_string) + 1
                #Optimization
                if (self.nBackspace == CharacterLimit):
                    self.resetEngine()
                    self.__preedit_string = unichr(keyval)
                    self.commitPreedit()
                    return True

                print "no. of fake backspace " + str(self.nBackspace)
                print "Old preedit:" + self.__preedit_string
                self.processChar(keyval)
                print "New Preedit:" + self.__preedit_string
                self.commitFakeBackspace()
                #self.commitPreedit()
                return True

        if self.__preedit_string:
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
                        self.commitPreedit()
                        self.isFakeBackspace = False
                        return True
                else:
                    print "A real backspace"
                    self.removeLastCharFromPreedit()
                return False

        self.resetEngine()
        return False

    def resetEngine(self):
        self.__preedit_string = u"";

    def __commit_string(self, text):
        self.commit_text(ibus.Text(text))

    def commitPreedit(self):
        self.__commit_string(self.__preedit_string)

    def processChar(self, char):
        self.addCharToPreedit(char)

    def addCharToPreedit(self, char):
        self.__preedit_string += unichr(char)

    def removeLastCharFromPreedit(self):
        self.__preedit_string = self.__preedit_string[:-1]

    def commitFakeBackspace(self):
        global dpy, BG_BACKSPACE
        print "Commit "+ str(self.nBackspace) + " fake Backspaces"
        number = self.nBackspace #Silly Python
        for i in range(number):
            Xtst.XTestFakeKeyEvent(dpy, BG_BACKSPACE, True, 0)
            Xtst.XTestFakeKeyEvent(dpy, BG_BACKSPACE, False, 0)
            Xlib.XFlush(dpy)

    def isCharacter(self, keyval):
        if keyval in xrange(33,126):
            return True
        else:
            return False
