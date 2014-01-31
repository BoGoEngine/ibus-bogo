#
# This file is part of ibus-bogo project.
#
# Copyright (C) 2012 Long T. Dam <longdt90@gmail.com>
# Copyright (C) 2012-2013 Trung Ngo <ndtrung4419@gmail.com>
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

from gi.repository import GObject
from gi.repository import IBus
from gi.repository import Gdk
import time
import logging
import os
import sys
from itertools import takewhile

ENGINE_PATH = os.path.dirname(__file__)
sys.path.append(
    os.path.abspath(os.path.join(ENGINE_PATH, "..")))

import bogo
from mouse_detector import MouseDetector
from focus_tracker import FocusTracker
from keysyms_mapping import mapping
from ui import UiDelegate
import vncharsets

vncharsets.init()


class BaseBackend():

    def reset(self):
        self.editing_string = ""
        self.raw_string = ""

    def update_composition(self, string):
        # Virtual method
        pass

    def commit_composition(self):
        # Virtual method
        pass

    def process_key_event(self, keyval, modifiers):
        if self.is_processable_key(keyval, modifiers):
            logging.debug("Key pressed: %c", chr(keyval))
            logging.debug("Raw string: %s", self.raw_string)
            logging.debug("Old string: %s", self.editing_string)

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
                logging.debug("Reverting brace shift")
                new_string = new_string[:-1] + \
                    chr(ord(new_string[-1]) - 0x20)

            logging.debug("New string: %s", new_string)

            self.update_composition(new_string)
            self.editing_string = new_string
            return True

        self.reset()
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
    #     logging.debug("Reset signal")
    #     self.reset()

    def is_processable_key(self, keyval, state):
        return \
            keyval in range(33, 126) and \
            not state & IBus.ModifierType.CONTROL_MASK and \
            not state & IBus.ModifierType.MOD1_MASK

    def on_backspace_pressed(self):
        logging.debug("Getting a backspace")
        if self.editing_string == "":
            return

        deleted_char = self.editing_string[-1]
        self.editing_string = self.editing_string[:-1]

        if len(self.editing_string) == 0:
            self.reset()
        else:
            index = self.raw_string.rfind(deleted_char)
            self.raw_string = self.raw_string[:-2] if index < 0 else \
                self.raw_string[:index] + \
                self.raw_string[(index + 1):]


class DirectEditBackend(BaseBackend):

    def __init__(self, engine, config, abbr_expander):
        self.engine = engine
        self.config = config
        self.abbr_expander = abbr_expander
        self.can_do_surrounding_text = False
        self.ever_checked_surrounding_text = False

        self.focus_tracker = FocusTracker()

    def reset(self):
        self.first_time_sending_backspace = True
        super().reset()

    def update_composition(self, string):
        self.commit_string(string)

    def commit_composition(self):
        self.commit_string(self.editing_string)

    def commit_string(self, string):
        same_initial_chars = list(takewhile(lambda tupl: tupl[0] == tupl[1],
                                            zip(self.editing_string,
                                                string)))

        n_backspace = len(self.editing_string) - len(same_initial_chars)
        string_to_commit = string[len(same_initial_chars):]

        self.delete_prev_chars(n_backspace)

        # Charset conversion
        # We encode a Unicode string into a byte sequence with the specified
        # encoding and then re-interpret it as a Unicode string containing
        # only latin-1 (ISO-8859-1) characters.
        #
        # This method has the flaw of not being able to commit raw legacy
        # encoding strings but it's the only thing we can do now as we cannot
        # commit bytes in Python 3, just Unicode string. Consider this example:
        #
        #     - UTF-8 'à': 0xc3 0xa0
        #     - TCVN3 'à': 0xb5 (rendered as '¶')
        #     - UTF-8 '¶': 0xc2 0xb6
        #
        # So if we typed 'à' in TCVN3, what the client receives would be
        # 0xc2 0xb6. Field testing shows that this does not affect LibreOffice
        # Writer and Kate (when forcing the file's encoding to be latin-1)
        # though.
        if self.engine.config['output-charset'] != 'utf-8':
            string_to_commit = string_to_commit \
                .encode(self.engine.config['output-charset']) \
                .decode('latin-1')

        # We cannot commit the text in Gtk since there is a bug in which
        # sometimes committed text comes before the forwarded
        # backspaces, resulting in undesirable output. Instead, we forward
        # each character to the current input context.
        #
        # We also need to detect whether the current input context is from a
        # GTK app by checking for the SURROUNDING_TEXT capability. It works
        # because as of right now (2013/02/22, IBus 1.4.1), only the IBus Gtk
        # client can do surrounding text.
        #
        # Very very veryyyy CRUDE, by the way.
        # if self.engine.input_context_capabilities & \
        #         IBus.Capabilite.SURROUNDING_TEXT:
        if False:
            logging.debug("Forwarding as commit...")

            for ch in string_to_commit:
                keyval = mapping[ch] if ch in mapping else ord(ch)
                self.engine.forward_key_event(keyval=keyval, keycode=0, state=0)
        else:
            logging.debug("Committing...")
            # Delaying to partially solve the synchronization issue.
            # Mostly for wine apps and for Gtk apps
            # when the above check doesn't work.
            time.sleep(0.005)
            self.engine.commit_text(IBus.Text.new_from_string(string_to_commit))

    def process_key_event(self, keyval, modifiers):
        # Check surrounding text capability after the first
        # keypress.
        if not self.ever_checked_surrounding_text and \
                len(self.raw_string) == 1:
            self.ever_checked_surrounding_text = True
            self.can_do_surrounding_text = self.check_surrounding_text()

        if keyval in [IBus.Return, IBus.BackSpace, IBus.space]:
            return self.on_special_key_pressed(keyval)

        eaten = super().process_key_event(keyval, modifiers)

        if eaten:
            self.update_composition(self.editing_string)

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
        self.focus_tracker.on_focus_changed()

    def delete_prev_chars_with_backspaces(self, count):
        if self.first_time_sending_backspace and \
                (self.focus_tracker.is_in_firefox() or
                 self.focus_tracker.is_in_chrome()):
            # Sending a dead space key to dismiss the
            # autocomplete box in Firefox and Chrome's
            # address bar. See:
            # https://github.com/BoGoEngine/ibus-bogo-python/pull/109
            logging.debug("Dismissing autocomplete...")

            self.engine.forward_key_event(IBus.space, 0, 0)
            self.engine.forward_key_event(IBus.BackSpace, 14, 0)

            self.first_time_sending_backspace = False

        for i in range(count):
            self.engine.forward_key_event(IBus.BackSpace, 14, 0)

    def delete_prev_chars(self, count):
        if count > 0:
            if self.can_do_surrounding_text and \
                    not self.focus_tracker.is_in_chrome():
                logging.debug("Deleting surrounding text...")
                self.engine.delete_surrounding_text(offset=-count, nchars=count)
            else:
                logging.debug("Sending backspace...")
                self.delete_prev_chars_with_backspaces(count)

    def on_special_key_pressed(self, keyval):
        if keyval == IBus.Return:
            self.reset()
            return False

        if keyval == IBus.BackSpace:
            self.on_backspace_pressed()
            return False

        if keyval == IBus.space:
            if self.config["enable-text-expansion"]:
                expanded_string = self.abbr_expander.expand(self.editing_string)

                if expanded_string != self.editing_string:
                    self.editing_string = expanded_string
                    self.commit_composition()
                    self.reset()
                    return False

            if self.config['skip-non-vietnamese'] and \
                    not bogo.validation.is_valid_string(
                        self.editing_string):
                self.editing_string = self.raw_string
                self.commit_composition()

            self.reset()
            return False


class Engine(IBus.Engine):
    __gtype_name__ = 'EngineBoGo'

    def __init__(self, config, abbr_expander):
        super(Engine, self).__init__()

        self.config = config
        self.ui_delegate = UiDelegate(engine=self)
        self.backend = DirectEditBackend(engine=self,
                                         config=config,
                                         abbr_expander=abbr_expander)

        # Create a new thread to detect mouse clicks
        mouse_detector = MouseDetector.get_instance()
        mouse_detector.add_mouse_click_listener(self.reset)

        self.input_context_capabilities = 0
        self.reset()

    def reset(self):
        self.backend.reset()

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
        # if self.focus_tracker.is_in_unity_dash():
        #     return False

        # Ignore key release events
        event_is_key_press = (modifiers & (1 << 30)) == 0

        # There is a strange overflow bug with python3-gi here so the above
        # line is used instead
        # is_press = ((modifiers & IBus.ModifierType.RELEASE_MASK) == 0)

        if not event_is_key_press:
            return False

        return self.backend.process_key_event(keyval, modifiers)

    def do_enable(self):
        self.ui_delegate.do_enable()
        self.backend.do_enable()

    def do_disable(self):
        self.reset()

    def do_focus_in(self):
        self.backend.do_focus_in()

    def do_focus_out(self):
        self.reset()

    def do_property_activate(self, prop_key, state):
        self.ui_delegate.do_property_activate(prop_key, state)

    def do_set_capabilities(self, caps):
        self.input_context_capabilities = caps
