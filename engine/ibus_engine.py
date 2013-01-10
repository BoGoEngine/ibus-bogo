#
# IBus-BoGo - The Vietnamese IME for IBus
#
# Copyright (c) 2012- Long T. Dam <longdt90@gmail.com>,
#                     Trung Ngo <ndtrung4419@gmail.com>
#
# This file is part of IBus-BoGo Project
# IBus-BoGo is free software: you can redistribute it and/or modify
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
import time
import logging

from bogo import new_bogo_engine as core
from config import Config

# Syntactic sugar
keysyms = IBus
modifier = IBus.ModifierType

# I know, I know. Singleton/global objects are horrible but
# right now there is no known way to pass more args to Engine
# because of how python-gobject works.
config = Config()

class Engine(IBus.Engine):
    __gtype_name__ = 'EngineBoGo'

    def __init__(self):
        super(Engine, self).__init__()
        self.__config = config
        self.commit_result = self.commit_utf8
        self.reset_engine()
        logging.info("You are running BoGo IBus Engine")

    # The "do_" part is PyGObject's way of overriding base's functions
    def do_process_key_event(self, keyval, keycode, state):
        """Implement IBus.Engine's process_key_event default signal handler.

        Args:
            keyval - The keycode, transformed through a keymap, stays the
                same for every keyboard
            keycode - Keyboard-dependant key code
            state - The state of modifier keys like Shift, Control, etc.
        Return:
            True - if successfully process the keyevent
            False - otherwise

        This function gets called whenever a key is pressed.
        """
        # ignore key release events
        is_press = ((state & IBus.ModifierType.RELEASE_MASK) == 0)
        if not is_press:
            return False

        if keyval == keysyms.Return or keyval == keysyms.Escape:
            self.reset_engine()
            return False

        if keyval == keysyms.BackSpace:
            self.new_string = self.new_string[:-1]
            # TODO A char in __raw_string doesn't equal a char in new_string
            self.__raw_string = self.__raw_string[:-1]
            if len(self.new_string) == 0:
                self.reset_engine()
            return False

        if self.is_character(keyval):
            # Process entered key here
            if state & (modifier.CONTROL_MASK | modifier.MOD1_MASK) == 0:
                self.__raw_string = self.__raw_string + chr(keyval)
                logging.debug("\nRaw string: %s" % self.__raw_string)
                
                case = 0
                cap = state & IBus.ModifierType.LOCK_MASK
                shift = state & IBus.ModifierType.SHIFT_MASK
                if (cap or shift) and not (cap and shift):
                    case = 1
                
                logging.debug("Key pressed: %c", chr(keyval))
                logging.debug("Old string: %s", self.old_string)
                self.old_string = self.new_string
                self.new_string = core.process_key(self.old_string,
                    chr(keyval),
                    case = case,
                    raw_string = self.__raw_string,
                    config = self.__config)
                
                logging.debug("New string: %s", self.new_string)
                self.number_fake_backspace, self.string_to_commit = \
                  self.get_nbackspace_and_string_to_commit()
                self.is_faking_backspace = True
                logging.debug("Number of fake backspace: %d", self.number_fake_backspace)
                logging.debug("String to commit: %s", self.string_to_commit)

                for i in range(self.number_fake_backspace):
                    self.forward_key_event(keysyms.BackSpace, 14, 0)

                # Sleep to ensure that all fake backspaces are committed.
                # Adjust time sleep to obtain proper behaviour
                time.sleep(0.015 * self.number_fake_backspace)
                self.commit_result(self.string_to_commit)
                time.sleep(0.003)
                return True

        if keyval == keysyms.space:
            logging.debug("Pressed a space")
            self.reset_engine()
            return False

        self.reset_engine()
        return False

    def reset_engine(self):
        self.string_to_commit = ""
        self.new_string = ""
        self.old_string = ""
        self.__raw_string = ""
        self.number_fake_backspace = 0

    def commit_utf8(self, string):
        self.commit_text(IBus.Text.new_from_string(string))

    def commit_tcvn3(self, string):
        tcvn3_string = BoGo.utf8_to_tcvn3(string)
        self.commit_text(IBus.Text.new_from_string(tcvn3_string))

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

    def is_character(self, keyval):
        return keyval in range(33,126)

    def do_focus_in(self):
        """Implements IBus.Engine's focus_in's default signal handler.

        Called when the input client widget gets focus.
        """
        self.register_properties(self.__config.prop_list)

    def do_focus_out(self):
        """Implements IBus.Engine's focus_out's default signal handler.

        Called when the input client widget loses focus.
        """
        self.reset_engine()

    def do_property_activate(self, prop_name, state):
        prop = self.__config.do_property_activate(prop_name, state)
        self.update_property(prop)
        self.reset_engine()
