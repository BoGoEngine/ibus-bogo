from nose.tools import eq_
from gi.repository import IBus
from ibus_engine.surrounding_text_backend import SurroundingTextBackend

try:
    from unittest.mock import Mock
except:
    from mock import Mock


class TestSurroundingTextBackend():

    def setup(self):
        self.engine = Mock()
        self.abbr_expander = Mock()
        self.auto_corrector = Mock()
        self.config = {}

        self.backend = SurroundingTextBackend(
            engine=self.engine,
            config=self.config,
            abbr_expander=self.abbr_expander,
            auto_corrector=self.auto_corrector)

    def test_update_composition(self):
        """
        update_composition() and commit_composition() should both use
        commit_string().
        """
        string = "blah"

        self.backend.commit_string = Mock()
        self.backend.update_composition(string)
        self.backend.commit_string.assert_called_once_with(string)

        self.backend.commit_string.reset_mock()
        self.backend.commit_composition(string)
        self.backend.commit_string.assert_called_once_with(string)

    def test_commit_string_surrounding_text(self):
        """
        commit_string() should delete the chars at the end of
        the input string that differs from the last input string
        using delete_surrounding_text() then commit only the diff.
        """
        prev_string = "blah"
        string = "bleo"
        diff_string = "eo"
        differ_len = 2

        self.engine.commit_text = Mock()
        self.backend.delete_prev_chars = Mock()

        self.backend.history.append({
            "type": "update-composition",
            "editing-string": prev_string,
            "raw-string": prev_string
        })
        self.backend.commit_string(string)

        self.backend.delete_prev_chars.assert_called_once_with(
            differ_len)
        eq_(self.engine.commit_text.call_args[0][0].text, diff_string)

    def test_backspace(self):
        """
        on_special_key_pressed() should not swallow a normal backspace.
        """
        self.backend.on_backspace_pressed = Mock()

        result = self.backend.on_special_key_pressed(IBus.BackSpace)

        expected = False
        eq_(result, expected)

    def test_backspace_undo(self):
        """
        on_special_key_pressed() should swallow the backspace if
        it is an undo.
        """
        self.backend.on_backspace_pressed = Mock()
        self.backend.reset = Mock()
        self.backend.history.append({
            "type": "undo"
        })

        result = self.backend.on_special_key_pressed(IBus.BackSpace)

        expected = True
        eq_(result, expected)
        self.backend.reset.assert_called_once()
