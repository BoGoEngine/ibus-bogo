from gi.repository import IBus
import logging
import bogo


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

    def on_space_pressed(self):
        if self.config["enable-text-expansion"]:
            expanded_string = self.abbr_expander.expand(self.editing_string)

            if expanded_string != self.editing_string:
                self.editing_string = expanded_string
                self.commit_composition()
                self.reset()
                return

        if self.config['skip-non-vietnamese'] and \
                not bogo.validation.is_valid_string(
                    self.editing_string):
            self.editing_string = self.raw_string
            self.commit_composition()
