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

from gi.repository import IBus, GObject
import logging
from collections import defaultdict
import bogo

logger = logging.getLogger(__name__)


class BaseBackend(GObject.Object):

    __gsignals__ = {
        'new_spellcheck_offender': (GObject.SIGNAL_RUN_LAST, bool,
                                    (str,))
    }

    def __init__(self, config, abbr_expander,
                 spellchecker, english_spellchecker):
        self.config = config
        self.abbr_expander = abbr_expander
        self.spellchecker = spellchecker
        self.english_spellchecker = english_spellchecker

        # History is a list/stack of 'action's, which can be commits,
        # backspaces, string expansions, string corrections, etc.
        self.history = []
        self.spell_offenders = defaultdict(lambda: 0)
        super().__init__()

    def last_nth_action(self, nth):
        if len(self.history) > nth:
            return self.history[-nth]
        else:
            return {
                "type": "none",
                "editing-string": "",
                "raw-string": ""
            }

    def last_action(self):
        return self.last_nth_action(1)

    def reset(self):
        self.editing_string = ""
        self.raw_string = ""

    def update_composition(self, string):
        self.history.append({
            "type": "update-composition",
            "raw-string": self.raw_string,
            "editing-string": self.editing_string
        })

    def commit_composition(self):
        self.history.append({
            "type": "commit-composition",
            "raw-string": self.raw_string,
            "editing-string": self.editing_string
        })

    def delete_prev_chars(self, count):
        self.history.append({
            "type": "delete-prev-chars",
            "raw-string": self.raw_string,
            "editing-string": self.editing_string
        })

    def process_key_event(self, keyval, modifiers):
        if self.is_processable_key(keyval, modifiers):
            logger.debug("Key pressed: %c", chr(keyval))
            logger.debug("Raw string: %s", self.raw_string)
            logger.debug("Old string: %s", self.editing_string)

            # Brace shift for TELEX's ][ keys.
            # When typing with capslock on, ][ won't get shifted to }{ resulting
            # in weird capitalization in "TưởNG". So we have to shift them
            # manually.
            keyval, brace_shift = self.do_brace_shift(keyval, modifiers)

            # Invoke BoGo to process the input
            new_string, self.raw_string = \
                bogo.process_key(string=self.editing_string,
                                 key=chr(keyval),
                                 fallback_sequence=self.raw_string,
                                 config=self.config)

            # Revert the brace shift
            if brace_shift and new_string and new_string[-1] in "{}":
                logger.debug("Reverting brace shift")
                new_string = new_string[:-1] + \
                    chr(ord(new_string[-1]) - 0x20)

            logger.debug("New string: %s", new_string)

            self.update_composition(new_string)
            self.editing_string = new_string
            return True
        else:
            return False

    def do_brace_shift(self, keyval, modifiers):
        capital_case = 0
        caps_lock = modifiers & IBus.ModifierType.LOCK_MASK
        shift = modifiers & IBus.ModifierType.SHIFT_MASK
        if (caps_lock or shift) and not (caps_lock and shift):
            capital_case = 1

        brace_shift = False
        if chr(keyval) in ['[', ']'] and capital_case == 1:
            keyval = keyval + 0x20
            brace_shift = True

        return keyval, brace_shift

    # This messes up Pidgin
    # def do_reset(self):
    #     logger.debug("Reset signal")
    #     self.reset()

    def is_processable_key(self, keyval, state):
        # We accept a-Z and all the keys used in the current
        # input mode.
        im_keys = self.config["default-input-methods"][self.config["input-method"]]
        return \
            not state & IBus.ModifierType.CONTROL_MASK and \
            not state & IBus.ModifierType.MOD1_MASK and \
            (keyval in range(65, 91) or 
             keyval in range(97, 123) or 
             keyval in im_keys)

    def undo_last_action(self):
        last_action = self.last_action()

        # If the last commited string is a spellchecker suggestion
        # then this backspace is to undo that. Three-time offenders
        # get blacklisted.
        if last_action["type"] == "string-correction":
            logging.debug("Undoing spell correction")

            # self.delete_prev_chars(1)
            self.editing_string = last_action["raw-string"]
            self.commit_composition()

            prev_raw_string = last_action["raw-string"]
            self.spell_offenders[prev_raw_string] += 1

            logging.debug("count = %s", self.spell_offenders[prev_raw_string])
            if self.spell_offenders[prev_raw_string] == 3:
                if self.emit(
                        'new_spellcheck_offender',
                        prev_raw_string):
                    self.spellchecker.add(prev_raw_string)
                else:
                    self.spell_offenders[prev_raw_string] = 0

            self.history.append({
                "type": "undo",
                "raw-string": self.raw_string,
                "editing-string": self.editing_string
            })

            self.reset()
            return True

        return False

    def on_backspace_pressed(self):
        logger.debug("Getting a backspace")
        if self.editing_string == "":
            self.reset()
            return False

        # Backspace is also the hotkey to undo the last action where
        # applicable.
        has_undone = self.undo_last_action()
        if has_undone:
            return True

        deleted_char = self.editing_string[-1]
        self.editing_string = self.editing_string[:-1]

        index = self.raw_string.rfind(deleted_char)
        self.raw_string = self.raw_string[:-2] if index < 0 else \
            self.raw_string[:index] + \
            self.raw_string[(index + 1):]

        return True

    def on_space_pressed(self):
        expanded_string = ""

        def can_expand():
            if self.config["enable-text-expansion"]:
                expanded_string = self.abbr_expander.expand(self.editing_string)
                return expanded_string != self.editing_string
            else:
                return False

        def is_non_vietnamese():
            if self.config['skip-non-vietnamese']:
                return not bogo.validation.is_valid_string(self.editing_string)
            else:
                return False

        # http://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
        def levenshtein(s1, s2):
            if len(s1) < len(s2):
                return levenshtein(s2, s1)
         
            # len(s1) >= len(s2)
            if len(s2) == 0:
                return len(s1)
         
            previous_row = range(len(s2) + 1)
            for i, c1 in enumerate(s1):
                current_row = [i + 1]
                for j, c2 in enumerate(s2):
                    insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
                    deletions = current_row[j] + 1       # than s2
                    substitutions = previous_row[j] + (c1 != c2)
                    current_row.append(min(insertions, deletions, substitutions))
                previous_row = current_row
 
            return previous_row[-1]

        if can_expand():
            self.editing_string = expanded_string
            self.update_composition(self.editing_string)

            self.history.append({
                "type": "string-expansion",
                "raw-string": self.raw_string,
                "editing-string": self.editing_string
            })
        elif is_non_vietnamese() \
                and not self.spellchecker.check(self.raw_string):
            try:
                suggested = self.spellchecker.suggest(self.raw_string)[0]
                max_distance = \
                    self.config["typo-correction-level"]
                distance = levenshtein(self.raw_string, suggested)

                if not self.english_spellchecker.check(self.raw_string) and \
                        distance <= max_distance:
                    self.editing_string = \
                        ' '.join(map(self.process_seq,
                                     suggested.split(' '))) + ' '
                    self.update_composition(self.editing_string)

                    self.history.append({
                        "type": "string-correction",
                        "raw-string": self.raw_string,
                        "editing-string": self.editing_string
                    })
            except IndexError:
                pass

    def process_seq(self, seq):
        string = ""
        raw = string
        for i in seq:
            string, raw = bogo.process_key(string,
                                           i,
                                           fallback_sequence=raw,
                                           config=self.config)
        return string
