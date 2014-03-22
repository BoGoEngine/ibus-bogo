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

import logging
import time
from itertools import takewhile
from gi.repository import IBus

import vncharsets
from base_backend import BaseBackend
from keysyms_mapping import mapping

vncharsets.init()


class SurroundingTextBackend(BaseBackend):

    """
    Backend for Engine that tries to directly manipulate the
    currently typing text inside the application being typed in.
    """

    def __init__(self, engine, config, abbr_expander):
        self.engine = engine
        self.config = config
        self.abbr_expander = abbr_expander
        self.reset()

    def reset(self):
        super().reset()
        self.previous_string = ""

    def update_composition(self, string):
        self.commit_string(string)

    def commit_composition(self):
        self.commit_string(self.editing_string)

    def commit_string(self, string):
        # Don't actually commit the whole string but only the part at the end
        # that differs from the editing_string
        same_initial_chars = list(takewhile(lambda tupl: tupl[0] == tupl[1],
                                            zip(self.previous_string,
                                                string)))

        n_backspace = len(self.previous_string) - len(same_initial_chars)
        string_to_commit = string[len(same_initial_chars):]

        logging.debug("Deleting %s chars...", n_backspace)
        self.delete_prev_chars(n_backspace)

        logging.debug("Committing: %s", string_to_commit)
        self.engine.commit_text(IBus.Text.new_from_string(string_to_commit))
        self.previous_string = string

    def process_key_event(self, keyval, modifiers):
        if keyval in [IBus.Return, IBus.BackSpace, IBus.space]:
            return self.on_special_key_pressed(keyval)

        if len(self.editing_string) == 0:
            # If we are not editing any word then try to process the
            # existing word at the cursor.
            surrounding_text, cursor, anchor = self.engine.get_surrounding_text()
            surrounding_text = surrounding_text.text[:cursor]

            # FIXME replace isalpha() with something like is_processable()
            if surrounding_text and surrounding_text[-1].isalpha():
                self.editing_string = surrounding_text.split(" ")[-1]
                self.previous_string = self.editing_string
                self.raw_string = self.editing_string

        eaten = super().process_key_event(keyval, modifiers)

        if eaten:
            self.update_composition(self.editing_string)
        else:
            self.reset()

        return eaten

    def check_surrounding_text(self):
        test_string = self.editing_string
        length = len(test_string)

        ibus_text, cursor_pos, anchor_pos = self.engine.get_surrounding_text()
        surrounding_text = ibus_text.get_text()

        if surrounding_text.endswith(test_string):
            self.engine.delete_surrounding_text(offset=-length, nchars=length)

            ibus_text, _, _ = self.engine.get_surrounding_text()
            surrounding_text = ibus_text.get_text()

            if not surrounding_text.endswith(test_string):
                self.engine.commit_text(
                    IBus.Text.new_from_string(test_string))
                return True
            else:
                return False

    def do_enable(self):
        # Notify the input context that we want to use surrounding
        # text.
        self.engine.get_surrounding_text()

    def do_focus_in(self):
        pass

    def delete_prev_chars(self, count):
        if count > 0:
            logging.debug("Deleting surrounding text...")
            self.engine.delete_surrounding_text(offset=-count, nchars=count)

    def on_special_key_pressed(self, keyval):
        if keyval == IBus.Return:
            self.reset()
            return False

        if keyval == IBus.BackSpace:
            self.on_backspace_pressed()
            self.previous_string = self.previous_string[:-1]
            return False

        if keyval == IBus.space:
            self.on_space_pressed()
            return False
