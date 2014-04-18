from nose.tools import eq_
from gi.repository import IBus
from surrounding_text_backend import SurroundingTextBackend
from base_backend import BackspaceType

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

    def test_delete_prev_chars(self):
        """
        delete_prev_chars() should use delete_surrounding_text()
        """
        count = 10
        self.engine.delete_surrounding_text = Mock()

        # Should do nothing with 0 count
        self.backend.delete_prev_chars(0)
        eq_(self.engine.delete_surrounding_text.called, False)

        self.backend.delete_prev_chars(count)
        self.engine.delete_surrounding_text.assert_called_once_with(
            offset=-count, nchars=count)

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
        self.backend.on_backspace_pressed = Mock(
            return_value=BackspaceType.UNDO)
        self.backend.reset = Mock()

        result = self.backend.on_special_key_pressed(IBus.BackSpace)

        expected = True
        eq_(result, expected)
        self.backend.reset.assert_called_once()

    def test_pick_up_surrounding_text(self):
        """
        process_key_event() should work with the surrounding text
        if possible.
        """
        surrounding_text = Mock()
        surrounding_text.text = "ao"
        cursor = 2
        anchor = 2
        key = "s"
        result = "áo"

        self.config["default-input-methods"] = {
            "my-im": {
                "s": "/"
            }
        }
        self.config["input-method"] = "my-im"

        self.engine.get_surrounding_text = \
            Mock(return_value=(surrounding_text, cursor, anchor))

        self.backend.process_key_event(ord(key), 0)

        self.engine.get_surrounding_text.assert_called_once()

        last_action = self.backend.last_action()
        expected = {
            "type": "update-composition",
            "editing-string": result,
            "raw-string": surrounding_text.text + key
        }
        eq_(last_action, expected)
