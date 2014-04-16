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
from itertools import takewhile
from gi.repository import IBus

import vncharsets
from base_backend import BaseBackend

vncharsets.init()
logger = logging.getLogger(__name__)


class SurroundingTextBackend(BaseBackend):

    """
    Backend for Engine that tries to directly manipulate the
    currently typing text inside the application being typed in.
    """

    def __init__(self, engine, config, abbr_expander,
                 auto_corrector):
        self.engine = engine

        super().__init__(
            config=config,
            abbr_expander=abbr_expander,
            auto_corrector=auto_corrector)
        self.reset()

    def reset(self):
        super().reset()

    def update_composition(self, string):
        self.commit_string(string)
        super().update_composition(string)

    def commit_composition(self):
        if len(self.editing_string) != 0:
            self.commit_string(self.editing_string)
            super().commit_composition()

    def commit_string(self, string):
        previous_string = self.last_action()["editing-string"]
        # Don't actually commit the whole string but only the part at the end
        # that differs from the editing_string
        same_initial_chars = list(takewhile(lambda tupl: tupl[0] == tupl[1],
                                            zip(previous_string,
                                                string)))

        n_backspace = len(previous_string) - len(same_initial_chars)
        string_to_commit = string[len(same_initial_chars):]

        logger.debug("Deleting %s chars...", n_backspace)
        self.delete_prev_chars(n_backspace)

        logger.debug("Committing: %s", string_to_commit)
        self.engine.commit_text(IBus.Text.new_from_string(string_to_commit))

    def process_key_event(self, keyval, modifiers):
        if keyval != IBus.BackSpace and \
                self.last_action()["type"] == "string-correction":
            self.reset()

        if keyval in [IBus.Return, IBus.BackSpace, IBus.space]:
            return self.on_special_key_pressed(keyval)

        if len(self.last_action()["editing-string"]) == 0:
            # If we are not editing any word then try to process the
            # existing word at the cursor.
            surrounding_text, cursor, anchor = \
                self.engine.get_surrounding_text()
            surrounding_text = surrounding_text.text[:cursor]

            # FIXME replace isalpha() with something like is_processable()
            if surrounding_text and surrounding_text[-1].isalpha():
                editing_string = surrounding_text.split(" ")[-1]
                self.history.append({
                    "type": "update-composition",
                    "editing-string": editing_string,
                    "raw-string": editing_string
                })

        eaten = super().process_key_event(keyval, modifiers)
        return eaten

    def do_enable(self):
        pass

    def do_focus_in(self):
        # Notify the input context that we want to use surrounding
        # text.
        # FIXME Maybe this should be in do_enable(), less DBus messages.
        self.engine.get_surrounding_text()

    def delete_prev_chars(self, count):
        if count > 0:
            logger.debug("Deleting surrounding text...")
            self.engine.delete_surrounding_text(offset=-count, nchars=count)
            super().delete_prev_chars(count)

    def on_special_key_pressed(self, keyval):
        if keyval == IBus.Return:
            self.reset()
            return False

        if keyval == IBus.BackSpace:
            self.on_backspace_pressed()

            last_action = self.last_action()
            if last_action["type"] == "undo":
                # The next backspace should be a normal backspace
                self.history.append({
                    "type": "none",
                    "editing-string": last_action["editing-string"],
                    "raw-string": last_action["raw-string"]
                })
                self.reset()
                return True
            else:
                return False

        if keyval == IBus.space:
            self.on_space_pressed()
            if self.last_action()["type"] == "string-correction":
                return True
            else:
                self.reset()
                return False
