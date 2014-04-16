from nose.tools import eq_
from ibus_engine.auto_corrector import AutoCorrector
from unittest.mock import Mock


class TestAutoCorrector():
    def setup(self):
        self.spellchecker = Mock()
        self.english_spellchecker = Mock()
        self.config = {
            "typo-correction-level": 2
        }

        self.corrector = AutoCorrector(
            config=self.config,
            spellchecker=self.spellchecker,
            english_spellchecker=self.english_spellchecker)

    def test_skip_blacklisted(self):
        """
        It should not auto-correct key sequences that are blacklisted.
        """
        # Blacklisted means spellchecker.check() returns True
        self.spellchecker.check = Mock(return_value=True)

        sequence = "carl"
        eq_(self.corrector.suggest(sequence), sequence)

    def test_no_suggestion(self):
        """
        It should return the input if there is no suggestion.
        """
        self.spellchecker.check = Mock(return_value=False)
        self.spellchecker.suggest = Mock(return_value=[])

        sequence = "carl"
        eq_(self.corrector.suggest(sequence), sequence)

    def test_missing_space(self):
        """
        It should correct 2 words joined together without space.
        """
        self.spellchecker.check = Mock(return_value=False)
        self.spellchecker.suggest = Mock(return_value=["cas meof"])
        self.english_spellchecker.check = Mock(return_value=False)

        sequence = "casmeof"
        result = "cá mèo"
        eq_(self.corrector.suggest(sequence), result)

    def test_level_zero_is_disable(self):
        """
        It should return the input if the typo correction level is
        zero.
        """
        self.spellchecker.check = Mock(return_value=False)
        self.spellchecker.suggest = Mock(return_value=["cas meof"])
        self.english_spellchecker.check = Mock(return_value=False)
        self.config["typo-correction-level"] = 0

        sequence = "casmeof"
        eq_(self.corrector.suggest(sequence), sequence)
