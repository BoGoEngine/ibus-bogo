import logging
import time
from itertools import takewhile
from gi.repository import IBus

from focus_tracker import FocusTracker
from base_backend import BaseBackend
from keysyms_mapping import mapping


class DirectEditBackend(BaseBackend):

    """
    Backend for Engine that tries to directly manipulate the
    currently typing text inside the application being typed in.
    """

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
        # Don't actually commit the whole string but only the part at the end
        # that differs from editing_string
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
            self.on_space_pressed()
            self.reset()
            return False
