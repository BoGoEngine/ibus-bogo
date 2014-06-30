from nose.tools import eq_
from auto_corrector import AutoCorrector

try:
    from unittest.mock import Mock
except:
    from mock import Mock


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

    def test_skip_english(self):
        """
        It should skip sequences that are deemed to be English
        by the English spellchecker.
        """
        self.spellchecker.check = Mock(return_value=False)
        self.spellchecker.suggest = Mock(return_value=["ser"])
        self.english_spellchecker.check = Mock(return_value=True)

        sequence = "set"
        eq_(self.corrector.suggest(sequence), sequence)

    def test_blacklist_after_n_offences(self):
        """
        It should blacklist a key sequence after N tickets. N is
        specified by the config dictionary.
        """
        self.spellchecker.check = Mock(return_value=False)
        self.spellchecker.suggest = Mock(return_value=["car"])

        self.config["typo-correction-threshold"] = 2

        sequence = "carl"

        for i in range(self.config["typo-correction-threshold"]):
            self.corrector.increase_ticket(sequence)

        self.spellchecker.add.assert_called_once_with(sequence)
