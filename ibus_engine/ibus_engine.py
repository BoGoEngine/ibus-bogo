# vim: set expandtab softtabstop=4 shiftwidth=4:
#
# This file is part of ibus-bogo project.
#
# Copyright (C) 2012 Long T. Dam <longdt90@gmail.com>
# Copyright (C) 2012-2014 Trung Ngo <ndtrung4419@gmail.com>
# Copyright (C) 2013 Duong H. Nguyen <cmpitg@gmail.com>
# Copyright (C) 2013 Hai P. Nguyen <hainp2604@gmail.com>
# Copyright (C) 2013-2014 Hai T. Nguyen <phaikawl@gmail.com>
#
# ibus-bogo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ibus-bogo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ibus-bogo.  If not, see <http://www.gnu.org/licenses/>.
#

from gi.repository import IBus
import os
import logging
import bogo


logger = logging.getLogger(__name__)

ENGINE_PATH = os.path.dirname(__file__)
DICT_PATH = ENGINE_PATH + '/data'
PWL_PATH = os.path.expanduser('~/.config/ibus-bogo/spelling-blacklist.txt')



punctuations = ".?!"


def text(string):
    return IBus.Text.new_from_string(string)


class Engine(IBus.Engine):
    __gtype_name__ = 'EngineBoGo'

    def __init__(self, config, abbr_expander):
        super().__init__()
        self.processing_string = ""
        self.key_sequence = ""

        self.reset()

    def reset(self):
        self.processing_string = ""
        self.key_sequence = ""
        self.hide_preedit_text()

    def commit(self):
        self.commit_text(text(self.processing_string))
        self.hide_preedit_text()

    # The "do_" part denotes a default signal handler
    def do_process_key_event(self, keyval, keycode, modifiers):
        """Implement IBus.Engine's process_key_event default signal handler.

        Args:
            keyval - The keycode, transformed through a keymap, stays the
                same for every keyboard
            keycode - Keyboard-dependant key code
            modifiers - The state of IBus.ModifierType keys like
                Shift, Control, etc.
        Return:
            True - if successfully process the keyevent
            False - otherwise

        This function gets called whenever a key is pressed.
        """

        # Ignore key release events
        event_is_key_press = (modifiers & (1 << 30)) == 0

        # There is a strange overflow bug with python3-gi here so the above
        # line is used instead
        # is_press = ((modifiers & IBus.ModifierType.RELEASE_MASK) == 0)

        if not event_is_key_press:
            return False

        if modifiers & (IBus.ModifierType.CONTROL_MASK |
                     IBus.ModifierType.MOD1_MASK) != 0:
            self.commit()
            self.reset()
            return False

        if self.is_processable_key(keyval, modifiers):
            if chr(keyval) in punctuations:
                self.commit()
                self.reset()
                return False

            self.key_sequence += chr(keyval)
            self.convert()
            self.update_preedit()

            return True
        else:
            return self.on_special_key_pressed(keyval)

    def convert(self):
        self.processing_string = bogo.process_sequence(self.key_sequence)

    def update_preedit(self):
        _text = text(self.processing_string)
        _text.append_attribute(type=IBus.AttrType.UNDERLINE,
                              value=IBus.AttrUnderline.SINGLE,
                              start_index=0,
                              end_index=len(self.processing_string))

        self.update_preedit_text_with_mode(
            _text,
            len(self.processing_string),
            True,
            IBus.PreeditFocusMode.COMMIT)
        self.show_preedit_text()

    def on_special_key_pressed(self, keyval):
        if keyval == IBus.BackSpace:
            if self.processing_string == "":
                self.hide_preedit_text()
                return False

            # deleted_char = self.processing_string[-1]
            # self.processing_string = self.processing_string[:-1]

            # index = self.key_sequence.rfind(deleted_char)
            # self.key_sequence = self.key_sequence[:-2] if index < 0 else \
            #     self.key_sequence[:index] + \
            #     self.key_sequence[(index + 1):]

            self.key_sequence = self.key_sequence[:-1]
            self.convert()
            self.update_preedit()
            return True

        # if keyval in [IBus.space, IBus.comma, IBus.semicolon, IBus.bracketright, IBus.period, IBus.quoteright]:
        #     self.on_space_pressed()
        #     if self.last_action()["type"] == "string-correction":
        #         return True

        self.commit()
        self.reset()
        return False


    def is_processable_key(self, keyval, state):
        return keyval in range(32, 126) and \
            state & (IBus.ModifierType.CONTROL_MASK |
                     IBus.ModifierType.MOD1_MASK) == 0

    def do_disable(self):
        self.reset()

    def do_focus_out(self):
        self.reset()

    def do_reset(self):
        self.reset()