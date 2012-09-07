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
import Xlib.display
import Xlib.X
import Xlib.XK
import Xlib.ext.xtest
import sys
import getopt
import time
import BoGo

# syntactic sugar
keysyms = IBus
modifier = IBus.ModifierType

dpy = Xlib.display.Display()
sym = Xlib.XK.string_to_keysym("BackSpace")
bg_backspace = dpy.keysym_to_keycode(sym)

class Engine(IBus.Engine):
    __gtype_name__ = 'EngineBoGo'

    def __init__(self):
        super(Engine, self).__init__()
        self.charset = self.get_charset_from_argument()
        if (self.charset == "TCVN3"):
            self.commit_result = self.commit_tcvn3
        else:
            self.commit_result = self.commit_utf8
        self.reset_engine()
        print "You are running BoGo Ibus Engine with charset " + self.charset


    # The "do_" part is PyGObject's way of overriding base's functions
    def do_process_key_event(self, keyval, keycode, state):
               # ignore key release events
        is_press = ((state & modifier.RELEASE_MASK) == 0)
        if not is_press:
            return True
	 
        if self.is_character(keyval):
            if state & (modifier.CONTROL_MASK | modifier.MOD1_MASK) == 0:
                print "Character entered: " + chr(keyval)
                self.is_fake_backspace = True

                self.old_string = self.new_string
                self.process_key(keyval)
                print "Old string:", self.old_string
                print "New string:", self.new_string
                self.n_backspace, self.string_to_commit = \
                  self.get_nbackspace_and_string_to_commit()
                self.n_backspace += 1
                print "n_backspace: ", self.n_backspace
                print "String to commit:", self.string_to_commit
                self.is_fake_backspace = True
                self.is_1st_fake_backspace = True
                self.time_to_sleep = 0.02 * (self.n_backspace - 1)
                self.commit_fake_backspace(self.n_backspace)
                return True

        if self.string_to_commit:
            if keyval == keysyms.Return or keyval == keysyms.Escape or\
               keyval == keysyms.space:
                self.reset_engine()
                return False

            if keyval == keysyms.BackSpace:
                if (self.is_fake_backspace):                
                    self.n_backspace -= 1  
                    if (self.n_backspace == 0):
                        time.sleep(self.time_to_sleep)
                        self.commit_result()
                        self.is_fake_backspace = False
                        return True
                    return False
                else:
                    self.remove_last_char()
                    return False

        self.reset_engine()
        return False

    def reset_engine(self):
        self.string_to_commit = u""
        self.new_string = u""
        self.old_string = u""
        self.is_fake_backspace = False
        self.is_1st_fake_backspace = False
        self.n_backspace = 0

    def commit_utf8(self):
        self.commit_text(IBus.Text.new_from_string(self.string_to_commit))
        
    def commit_tcvn3(self):
        tcvn3_string = BoGo.utf8_to_tcvn3(self.string_to_commit)
        self.commit_text(IBus.Text.new_from_string(tcvn3_string))

    def process_key(self, keyval):
        uni_keyval = unichr(keyval)
        if self.old_string:
            print BoGo.process_key(self.old_string, uni_keyval)
            self.new_string = BoGo.process_key(self.old_string, uni_keyval)
        else:
            self.new_string = uni_keyval

    def remove_last_char(self):
        self.new_string = self.new_string[:-1]

    def commit_fake_backspace(self,n_backspace):
        for i in range(n_backspace):
            Xlib.ext.xtest.fake_input(dpy, Xlib.X.KeyPress, bg_backspace)
            Xlib.ext.xtest.fake_input(dpy, Xlib.X.KeyRelease, bg_backspace)
            dpy.flush()

    def get_nbackspace_and_string_to_commit(self):
        if (self.old_string):
            length = len(self.old_string)
            for i in range(length):
                if self.old_string[i] != self.new_string[i]:
                    _nbackspace = length - i
                    _stringtocommit = self.new_string[i:]
                    return _nbackspace, _stringtocommit
            return 0, self.new_string[length:]
        else:
             return 0, self.new_string
        # Classical method:
        # return len(self.old_string) + 1, self.new_string

    def is_character(self, keyval):
        if keyval in xrange(33,126):
            return True
        else:
            return False

    def is_ending_character(self, keyval):
        pass

    def get_charset_from_argument(self):
        shortopt = "ihdut"
        longopt = ["ibus", "help", "daemonize", "utf8", "tcvn3"]

        try:
            opts, args = getopt.getopt(sys.argv[1:], shortopt, longopt)
        except getopt.GetoptError, err:
            print_help(sys.stderr, 1)

        for o, a in opts:
            if o in ("-t", "--tcvn3"):
                return "TCVN3"
        return "UTF8"
