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
import subprocess
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
import vncharsets

vncharsets.init()


def string_to_ibus_text(string):
    return IBus.Text.new_from_string(string)


def ibus_text_to_string(text):
    return text.get_text()


class Engine(IBus.Engine):
    __gtype_name__ = 'EngineBoGo'

    def __init__(self, config, abbr_expander):
        super(Engine, self).__init__()
        self.config = config
        self.input_context_capabilities = 0
        self.setup_tool_buttons()

        self.abbr_expander = abbr_expander

        self.can_do_surrounding_text = False
        self.ever_checked_surrounding_text = False
        self.reset_engine()

        # Create a new thread to detect mouse clicks
        mouse_detector = MouseDetector.get_instance()
        mouse_detector.add_mouse_click_listener(self.reset_engine)

        self.focus_tracker = FocusTracker()

    def reset_engine(self):
        self.new_string = ""
        self.prev_string = ""
        self.raw_string = ""
        self.first_time_sending_backspace = True

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
        if self.focus_tracker.is_in_unity_dash():
            return False

        # Ignore key release events
        event_is_key_press = (modifiers & (1 << 30)) == 0

        # There is a strange overflow bug with python3-gi here so the above
        # line is used instead
        # is_press = ((modifiers & IBus.ModifierType.RELEASE_MASK) == 0)

        if not event_is_key_press:
            return False

        if keyval in [IBus.Return, IBus.BackSpace, IBus.space]:
            return self.on_special_key_pressed(keyval)

        # Check surrounding text capability after the first
        # keypress.
        if not self.ever_checked_surrounding_text and \
                len(self.raw_string) == 1:
            self.ever_checked_surrounding_text = True
            self.can_do_surrounding_text = self.check_surrounding_text()

        if self.is_processable_key(keyval, modifiers):
            logging.debug("Key pressed: %c", chr(keyval))
            logging.debug("Raw string: %s", self.raw_string)
            logging.debug("Old string: %s", self.prev_string)

            # Brace shift for TELEX's ][ keys.
            # When typing with capslock on, ][ won't get shifted to }{ resulting
            # in weird capitalization in "TưởNG". So we have to shift them
            # manually.
            keyval, brace_shift = self.do_brace_shift(keyval, modifiers)

            # Invoke BoGo to process the input
            self.new_string, self.raw_string = \
                bogo.process_key(string=self.prev_string,
                                 key=chr(keyval),
                                 fallback_sequence=self.raw_string,
                                 config=self.config)

            # Revert the brace shift
            if brace_shift and self.new_string and self.new_string[-1] in "{}":
                logging.debug("Reverting brace shift")
                self.new_string = self.new_string[:-1] + \
                    chr(ord(self.new_string[-1]) - 0x20)

            logging.debug("New string: %s", self.new_string)

            self.commit_result(self.new_string)
            self.prev_string = self.new_string
            return True

        self.reset_engine()
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
    #     self.reset_engine()

    def commit_result(self, string):
        same_initial_chars = list(takewhile(lambda tupl: tupl[0] == tupl[1],
                                            zip(self.prev_string,
                                                self.new_string)))

        n_backspace = len(self.prev_string) - len(same_initial_chars)
        string_to_commit = self.new_string[len(same_initial_chars):]

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
        if self.config['output-charset'] != 'utf-8':
            string_to_commit = string_to_commit \
                .encode(self.config['output-charset']) \
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
        if self.input_context_capabilities & IBus.Capabilite.SURROUNDING_TEXT:
            logging.debug("Forwarding as commit...")

            for ch in string_to_commit:
                keyval = mapping[ch] if ch in mapping else ord(ch)
                self.forward_key_event(keyval=keyval, keycode=0, state=0)
        else:
            logging.debug("Committing...")
            # Delaying to partially solve the synchronization issue.
            # Mostly for wine apps and for Gtk apps
            # when the above check doesn't work.
            time.sleep(0.005)
            self.commit_text(string_to_ibus_text(string_to_commit))

        self.current_shown_text = string

    def is_processable_key(self, keyval, state):
        # This can be extended to support typing in French, Japanese,...
        # keyboards. But currently not working.
        #
        # TODO Don't assume default-input-methods
        IMs = self.config['default-input-methods']
        current_im = IMs[self.config['input-method']]

        key = chr(keyval)
        return keyval in range(33, 126) and \
            state & (IBus.ModifierType.CONTROL_MASK |
                     IBus.ModifierType.MOD1_MASK) == 0 and \
            (key.isalpha() or key in current_im.keys())

    def check_surrounding_text(self):
        length = len(self.prev_string)

        text, cursor_pos, anchor_pos = self.get_surrounding_text()
        surrounding_text = ibus_text_to_string(text)

        if surrounding_text.endswith(self.prev_string):
            self.delete_surrounding_text(offset=-length, nchars=length)

            text, cursor_pos, anchor_pos = self.get_surrounding_text()
            surrounding_text = ibus_text_to_string(text)

            if not surrounding_text.endswith(self.prev_string):
                self.commit_text(string_to_ibus_text(self.prev_string))
                return True
            else:
                return False

    def delete_prev_chars_with_backspaces(self, count):
        if self.first_time_sending_backspace and \
                (self.focus_tracker.is_in_firefox() or
                 self.focus_tracker.is_in_chrome()):
            # Sending a dead space key to dismiss the
            # autocomplete box in Firefox and Chrome's
            # address bar. See:
            # https://github.com/BoGoEngine/ibus-bogo-python/pull/109
            logging.debug("Dismissing autocomplete...")

            self.forward_key_event(IBus.space, 0, 0)
            self.forward_key_event(IBus.BackSpace, 14, 0)

            self.first_time_sending_backspace = False

        for i in range(count):
            self.forward_key_event(IBus.BackSpace, 14, 0)

    def delete_prev_chars(self, count):
        if count > 0:
            if self.can_do_surrounding_text and \
                    not self.focus_tracker.is_in_chrome():
                logging.debug("Deleting surrounding text...")
                self.delete_surrounding_text(offset=-count, nchars=count)
            else:
                logging.debug("Sending backspace...")
                self.delete_prev_chars_with_backspaces(count)

    def setup_tool_buttons(self):
        self.prop_list = IBus.PropList()
        label = string_to_ibus_text("Preferences")
        tooltip = label
        pref_button = IBus.Property.new(key="preferences",
                                        type=IBus.PropType.NORMAL,
                                        label=label,
                                        icon="preferences-other",
                                        tooltip=tooltip,
                                        sensitive=True,
                                        visible=True,
                                        state=0,
                                        prop_list=None)
        help_button = IBus.Property.new(key="help",
                                        type=IBus.PropType.NORMAL,
                                        label=string_to_ibus_text("Help"),
                                        icon="system-help",
                                        tooltip=string_to_ibus_text("Help"),
                                        sensitive=True,
                                        visible=True,
                                        state=0,
                                        prop_list=None)
        self.prop_list.append(pref_button)
        self.prop_list.append(help_button)

    def do_enable(self):
        pass

    def do_disable(self):
        self.reset_engine()

    def do_focus_in(self):
        """Implements IBus.Engine's focus_in's default signal handler.

        Called when the input client widget gets focus.
        """
        self.register_properties(self.prop_list)
        self.focus_tracker.on_focus_changed()

    def do_focus_out(self):
        """Implements IBus.Engine's focus_out's default signal handler.

        Called when the input client widget loses focus.
        """
        self.reset_engine()

    def do_property_activate(self, prop_key, state):
        if prop_key == "preferences":
            try:
                pid = os.fork()
                if pid == 0:
                    # os.system("/usr/lib/ibus-bogo/ibus-bogo-settings")
                    os.system("python3 " +
                              os.path.join(os.path.dirname(__file__),
                                           "..",
                                           "gui/controller.py"))
                    os._exit(0)
            except:
                pass
        elif prop_key == "help":
            link = "http://ibus-bogo.readthedocs.org/en/latest/usage.html"
            subprocess.call("xdg-open " + link, shell=True)
        self.reset_engine()

    def do_set_capabilities(self, caps):
        self.input_context_capabilities = caps

    def on_special_key_pressed(self, keyval):
        if keyval == IBus.Return:
            self.reset_engine()
            return False

        if keyval == IBus.BackSpace:
            logging.debug("Getting a backspace")
            if self.new_string == "":
                return False

            deleted_char = self.new_string[-1]
            self.new_string = self.new_string[:-1]
            self.current_shown_text = self.new_string
            self.prev_string = self.new_string

            if len(self.new_string) == 0:
                self.reset_engine()
            else:
                index = self.raw_string.rfind(deleted_char)
                self.raw_string = self.raw_string[:-2] if index < 0 else \
                    self.raw_string[:index] + \
                    self.raw_string[(index + 1):]

            return False

        if keyval == IBus.space:
            if self.config["enable-text-expansion"]:
                expanded_string = self.abbr_expander.expand(self.prev_string)

                if expanded_string != self.prev_string:
                    self.commit_result(expanded_string)
                    self.reset_engine()
                    return False

            if self.config['skip-non-vietnamese'] and \
                    not bogo.validation.is_valid_string(self.prev_string):
                self.commit_result(self.raw_string)

            self.reset_engine()
            return False
