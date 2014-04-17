from nose.tools import eq_
from ibus_engine.base_backend import BaseBackend

try:
    from unittest.mock import Mock
except:
    from mock import Mock


class TestBaseBackend():

    def setup(self):
        self.expander = Mock()
        self.corrector = Mock()
        self.config = {}

        self.backend = BaseBackend(
            config=self.config,
            abbr_expander=self.expander,
            auto_corrector=self.corrector)

    def test_update_composition(self):
        """
        update_composition() should create a new history entry.
        """
        string = "blah"

        self.backend.update_composition(string)

        expected = {
            "type": "update-composition",
            "raw-string": "",
            "editing-string": string
        }

        eq_(self.backend.last_action(), expected)

    def test_commit_composition(self):
        """
        commit_composition() should create a new history entry based on
        self.editing_string.
        """

        string = "blah"

        self.backend.commit_composition(string)

        expected = {
            "type": "commit-composition",
            "raw-string": "",
            "editing-string": string
        }

        eq_(self.backend.last_action(), expected)

    def test_text_expansion(self):
        """
        It should expand text if possible and allowed on space key press.
        FIXME: Just space key?
        """
        string = "bl"
        expanded = "blah"

        self.expander.expand = Mock(return_value=expanded)
        self.config["enable-text-expansion"] = True
        self.backend.update_composition = Mock()

        self.backend.editing_string = string
        self.backend.on_space_pressed()

        expected = {
            "type": "string-expansion",
            "raw-string": "",
            "editing-string": expanded
        }

        eq_(self.backend.last_action(), expected)
        self.backend.update_composition.assert_called_once_with(expanded)

    def test_reset(self):
        """
        reset() should create a history entry.
        """
        self.backend.reset()

        expected = {
            "type": "reset",
            "raw-string": "",
            "editing-string": ""
        }

        eq_(self.backend.last_action(), expected)
