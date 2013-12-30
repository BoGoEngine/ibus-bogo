#
# This file is part of ibus-bogo-python project.
#
# Copyright (C) 2012 Long T. Dam <longdt90@gmail.com>
# Copyright (C) 2012-2013 Trung Ngo <ndtrung4419@gmail.com>
# Copyright (C) 2013 Duong H. Nguyen <cmpitg@gmail.com>
# Copyright (C) 2013 Hai P. Nguyen <hainp2604@gmail.com>
#
# ibus-bogo-python is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ibus-bogo-python is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ibus-bogo-python.  If not, see <http://www.gnu.org/licenses/>.
#

from gi.repository import GObject
from gi.repository import IBus
from gi.repository import Gdk
from gi.repository import Wnck
import time
import logging
import subprocess
import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import bogo
from config import Config
from keysyms_mapping import mapping

import vncharsets
vncharsets.init()


# Since we don't instantiate the Engine class ourselves (IBus does), we can't
# inject a Config object into it. Therefore, we have to resort to using a global
# object like this.
#
# TODO: We should be able to subclass
# IBusFactory and pre-apply the config object as an argument to
# our engine's constructor.
config = Config()


def string_to_text(string):
    return IBus.Text.new_from_string(string)


def check_unity():
    try:
        screen = Wnck.Screen.get_default()
        screen.force_update()
        window = screen.get_active_window()
        window_name = window.get_name()
        window_type = window.get_window_type()
        logging.info("Current active window: %s" % window_name)
        if window_type == Wnck.WindowType.DOCK and \
                (window_name == 'launcher' or
                 window_name == 'unity-dash'):
            return True
        else:
            return False
    except:
        return False


class Engine(IBus.Engine):
    __gtype_name__ = 'EngineBoGo'

    def __init__(self):
        super(Engine, self).__init__()
        logging.info("You are running ibus-bogo-python")

        self.__config = config
        self.input_context_capabilities = 0
        self.is_in_unity = check_unity()

        self.lookup_table = IBus.LookupTable()
        self.lookup_table.set_page_size(4)
        self.lookup_table.set_orientation(1)
        self.lookup_table.set_cursor_visible(True)
        self.is_lookup_table_shown = False

        self.setup_tool_buttons()

        self.reset_engine()

    # The "do_" part is PyGObject's way of overriding base's functions
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
        if self.is_in_unity is True:
            return False

        # Ignore key release events
        event_is_key_press = (modifiers & (1 << 30)) == 0  # There's a strange

        # There is a strange overflow bug with python3-gi here so the above
        # line is used instead
        # is_press = ((modifiers & IBus.ModifierType.RELEASE_MASK) == 0)

        if not event_is_key_press:
            return False

        if keyval == IBus.Return:
            return self.on_return_pressed()

        if keyval in [IBus.Up, IBus.Down]:
            return self.on_updown_pressed(keyval)

        if keyval == IBus.BackSpace:
            return self.on_backspace_pressed()

        if self.is_processable_key(keyval, modifiers):
            logging.debug("Key pressed: %c", chr(keyval))
            logging.debug("Raw string: %s", self.__raw_string)
            logging.debug("Old string: %s", self.old_string)

            # Brace shift for TELEX's ][ keys.
            # When typing with capslock on, ][ won't get shifted to }{ resulting
            # in weird capitalization in "TưởNG". So we have to shift them
            # manually.
            keyval, brace_shift = self.do_brace_shift(keyval, modifiers)

            # Call Bogo engine to process the input
            self.new_string, self.__raw_string = \
                bogo.process_key(self.old_string,
                                 chr(keyval),
                                 fallback_sequence=self.__raw_string,
                                 config=self.__config)

            if self.__config['skip-non-vietnamese']:
                # Detect if the raw input sequence can produce a syntactically
                # legitimate Vietnamese word by putting it through
                # bogo.process_key() twice, first with skip-non-vietnamese on,
                # then with that setting off. If the two results differ then
                # the sequence cannot produce a correct Vietnamse word.
                #
                # Eg:
                #   `system` -> system != sýtem   | bad
                #   `ba`     -> ba     == ba      | good
                #   `meof`   -> mèo    == mèo     | good
                if not self.stubborn_old_string:
                    self.stubborn_old_string = self.old_string
                else:
                    self.stubborn_old_string = self.stubborn_new_string
                stubborn_config = dict(self.__config.items())
                stubborn_config['skip-non-vietnamese'] = False
                self.stubborn_new_string = \
                    bogo.process_key(self.stubborn_old_string,
                                     chr(keyval),
                                     config=stubborn_config)[0]

                if self.stubborn_new_string != self.new_string:
                    # The key sequence cannot generate a correct Vietnamese
                    # word. But we will offer the user the incorrect word
                    # as an option.
                    self.lookup_table.clear()
                    self.lookup_table.append_candidate(
                        string_to_text(self.new_string))
                    self.lookup_table.append_candidate(
                        string_to_text(self.stubborn_new_string))

                    # Urge IBus to put the lookup table at the correct location.
                    # Despite this call, no pre-editing is shown.
                    self.show_preedit_text()

                    self.update_lookup_table(self.lookup_table, True)
                    self.show_lookup_table()
                    self.is_lookup_table_shown = True

            # Revert the brace shift
            if brace_shift and self.new_string and self.new_string[-1] in "{}":
                logging.debug("Reverting brace shift")
                self.new_string = self.new_string[:-1] + \
                    chr(ord(self.new_string[-1]) - 0x20)

            logging.debug("New string: %s", self.new_string)

            self.commit_result(self.new_string)
            self.old_string = self.new_string

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

    def reset_engine(self):
        self.new_string = ""
        self.old_string = ""
        self.__raw_string = ""
        self.stubborn_old_string = ""
        self.stubborn_new_string = ""
        self.current_shown_text = ""
        self.hide_lookup_table()
        self.hide_preedit_text()
        self.lookup_table.clear()
        self.is_lookup_table_shown = False
        self.is_table_dirty = False

    def commit_result(self, string):
        def get_nbackspace_and_string_to_commit(old_string, new_string):
            if (old_string):
                length = len(old_string)
                for i in range(length):
                    if old_string[i] != new_string[i]:
                        _nbackspace = length - i
                        _stringtocommit = new_string[i:]
                        return _nbackspace, _stringtocommit
                return 0, new_string[length:]
            else:
                return 0, new_string

        number_fake_backspace, string_to_commit = \
            get_nbackspace_and_string_to_commit(self.current_shown_text, string)
        logging.debug("Number of fake backspace: %d", number_fake_backspace)
        logging.debug("String to commit: %s", string_to_commit)

        for i in range(number_fake_backspace):
            self.forward_key_event(IBus.BackSpace, 14, 0)

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
        if config['output-charset'] != 'utf-8':
            string_to_commit = string_to_commit \
                .encode(config['output-charset']) \
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
            logging.debug("forwarding as commit")

            for ch in string_to_commit:
                self.forward_key_event(
                    mapping[ch] if ch in mapping else ord(ch),
                    0,
                    0
                )
        else:
            logging.debug("Committing")
            # Delaying to partially solve the synchronization issue.
            # Mostly for wine apps and for Gtk apps
            # when the above check doesn't work.
            time.sleep(0.005)
            self.commit_text(string_to_text(string_to_commit))

        self.current_shown_text = string

    def is_processable_key(self, keyval, state):
        # This can be extended to support typing in French, Japanese,...
        # keyboards. But currently not working.
        #
        # TODO Don't assume default-input-methods
        current_im = config['default-input-methods'][config['input-method']]

        key = chr(keyval)
        return keyval in range(33, 126) and \
            state & (IBus.ModifierType.CONTROL_MASK |
                     IBus.ModifierType.MOD1_MASK) == 0 and \
            (key.isalpha() or key in current_im.keys())

    def setup_tool_buttons(self):
        self.prop_list = IBus.PropList()
        pref_button = IBus.Property.new(key="preferences",
                                        type=IBus.PropType.NORMAL,
                                        label=string_to_text("Pref"),
                                        icon="preferences-other",
                                        tooltip=string_to_text("Preferences"),
                                        sensitive=True,
                                        visible=True,
                                        state=0,
                                        prop_list=None)
        help_button = IBus.Property.new(key="help",
                                        type=IBus.PropType.NORMAL,
                                        label=string_to_text("Help"),
                                        icon="system-help",
                                        tooltip=string_to_text("Help"),
                                        sensitive=True,
                                        visible=True,
                                        state=0,
                                        prop_list=None)
        self.prop_list.append(pref_button)
        self.prop_list.append(help_button)

    def do_enable(self):
        pass

    def do_disable(self):
        pass

    def do_focus_in(self):
        """Implements IBus.Engine's focus_in's default signal handler.

        Called when the input client widget gets focus.
        """
        self.register_properties(self.prop_list)

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
                                           "config-gui/controller.py"))
                    os._exit(0)
            except:
                pass
        elif prop_key == "help":
            link = "http://ibus-bogo.readthedocs.org/en/latest/usage.html"
            subprocess.call("xdg-open " + link, shell=True)
        self.reset_engine()

    def do_set_capabilities(self, caps):
        self.input_context_capabilities = caps

    def do_candidate_clicked(self):
        pass

    def on_return_pressed(self):
        if self.stubborn_new_string and \
                self.is_lookup_table_shown and \
                self.is_table_dirty:
            self.old_string = self.new_string
            self.commit_result(self.lookup_table.get_candidate(
                self.lookup_table.get_cursor_pos()).get_text())
            self.reset_engine()
            return True
        else:
            self.reset_engine()
            return False

    def on_updown_pressed(self, key):
        key = {IBus.Up: "up", IBus.Down: "down"}[key]
        if self.is_lookup_table_shown:
            getattr(self.lookup_table, "cursor_" + key)()
            self.update_lookup_table(self.lookup_table, True)
            self.commit_result(self.lookup_table.get_candidate(
                self.lookup_table.get_cursor_pos()).get_text())
            self.is_table_dirty = True
            return True
        else:
            return False

    def on_backspace_pressed(self):
        logging.debug("Getting a backspace")
        self.new_string = self.new_string[:-1]
        self.current_shown_text = self.new_string
        # TODO A char in __raw_string doesn't equal a char in new_string
        self.__raw_string = self.__raw_string[:-1]
        if len(self.new_string) == 0:
            self.reset_engine()
        return False
