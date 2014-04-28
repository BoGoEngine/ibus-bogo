from nose.tools import eq_
from gi.repository import IBus
from preedit_backend import PreeditBackend

try:
    from unittest.mock import Mock
except:
    from mock import Mock


class TestPreeditBackend():

    def setup(self):
        self.engine = Mock()
        self.config = {}
        self.abbr_expander = Mock()
        self.auto_corrector = Mock()

        self.backend = PreeditBackend(
            engine=self.engine,
            config=self.config,
            abbr_expander=self.abbr_expander,
            auto_corrector=self.auto_corrector)

    def test_update_composition_preedit(self):
        """
        update_composition() should use preedit.
        """
        string = "blah"
        self.engine.update_preedit_text_with_mode = Mock()

        self.backend.update_composition(string)

        self.engine.update_preedit_text_with_mode.assert_called_once()
        args = self.engine.update_preedit_text_with_mode.call_args[1]

        eq_(args["text"].text, string)

    def test_commit_last_correction(self):
        """
        Should commit the last string correction preedit text
        on the next normal key press.
        """
        corrected_string = "ba"
        key = "a"

        self.backend.history.append({
            "type": "string-correction",
            "editing-string": corrected_string,
            "raw-string": "bah"
        })

        self.config["input-method-definition"] = {}
        self.config["input-method"] = "aoe"

        self.backend.commit_composition = Mock()
        self.backend.update_composition = Mock()

        self.backend.process_key_event(ord(key), 0)

        self.backend.commit_composition.assert_called_once_with(
            corrected_string)
        self.backend.update_composition.assert_called_once_with(
            string=key, raw_string=key)

    def test_backspace_preedit(self):
        """
        If there is a preedit showing then it should update the preedit
        with one less character, else it should yield a hard backspace.
        """
        self.backend.update_composition = Mock()
        self.backend.reset = Mock()

        self.backend.history.append({
            "type": "update-composition",
            "editing-string": "a",
            "raw-string": "a"
        })

        result = self.backend.on_special_key_pressed(IBus.BackSpace)

        eq_(result, True)
        self.backend.update_composition.assert_called_once_with("")
