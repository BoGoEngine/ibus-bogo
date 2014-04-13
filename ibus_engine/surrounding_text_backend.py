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
from collections import defaultdict
from gi.repository import IBus, GObject

import vncharsets
from base_backend import BaseBackend

vncharsets.init()
logger = logging.getLogger(__name__)


class SurroundingTextBackend(BaseBackend, GObject.GObject):

    """
    Backend for Engine that tries to directly manipulate the
    currently typing text inside the application being typed in.
    """

    __gsignals__ = {
        'new_spellcheck_offender': (GObject.SIGNAL_RUN_LAST, bool,
                                    (str,))
    }

    def __init__(self, engine, config, abbr_expander, spellchecker):
        self.engine = engine
        self.config = config
        self.abbr_expander = abbr_expander
        self.spellchecker = spellchecker

        self.spell_offenders = defaultdict(lambda: 0)

        super().__init__()
        self.reset()

    def reset(self):
        super().reset()
        self.previous_string = ""

    def update_composition(self, string):
        self.commit_string(string)

    def commit_composition(self):
        if len(self.editing_string) != 0:
            self.commit_string(self.editing_string)

    def commit_string(self, string):
        # Don't actually commit the whole string but only the part at the end
        # that differs from the editing_string
        same_initial_chars = list(takewhile(lambda tupl: tupl[0] == tupl[1],
                                            zip(self.previous_string,
                                                string)))

        n_backspace = len(self.previous_string) - len(same_initial_chars)
        string_to_commit = string[len(same_initial_chars):]

        logger.debug("Deleting %s chars...", n_backspace)
        self.delete_prev_chars(n_backspace)

        logger.debug("Committing: %s", string_to_commit)
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

    def on_special_key_pressed(self, keyval):
        if keyval == IBus.Return:
            self.reset()
            return False

        if keyval == IBus.BackSpace:
            # If the last commited string is a spellchecker suggestion
            # then this backspace is to undo that. Three-time offenders
            # get blacklisted.
            if self.suggested_spell:
                # Delete the space character
                self.delete_prev_chars(1)

                self.editing_string = self.prev_raw_string
                self.commit_composition()
                self.suggested_spell = False

                self.spell_offenders[self.prev_raw_string] += 1

                if self.spell_offenders[self.prev_raw_string] == 3:
                    if self.emit(
                            'new_spellcheck_offender',
                            self.prev_raw_string):
                        self.spellchecker.add(self.prev_raw_string)
                    else:
                        self.spell_offenders[self.prev_raw_string] = 0

                self.reset()
                return True

            self.on_backspace_pressed()
            self.previous_string = self.previous_string[:-1]
            return False

        if keyval == IBus.space:
            self.on_space_pressed()
            self.commit_composition()
            if not self.suggested_spell:
                self.reset()
            return False
