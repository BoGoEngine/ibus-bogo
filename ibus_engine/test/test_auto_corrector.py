from nose.tools import eq_
from ibus_engine.auto_corrector import AutoCorrector

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

        on_new_spellcheck_offender = Mock(return_value=True)
        self.corrector.connect(
            "new_spellcheck_offender", on_new_spellcheck_offender)

        sequence = "carl"
        self.corrector.increase_ticket(sequence)
        self.corrector.increase_ticket(sequence)
        self.corrector.increase_ticket(sequence)

        on_new_spellcheck_offender.assert_called_once_with(
            self.corrector, sequence)
        self.spellchecker.add.assert_called_once_with(sequence)

    def test_dont_blacklist(self):
        """
        It should not blacklist a key sequence if the last
        signal handler for new_spellcheck_offender returns False.
        """
        self.spellchecker.check = Mock(return_value=False)
        self.spellchecker.suggest = Mock(return_value=["car"])

        on_new_spellcheck_offender = Mock(return_value=False)
        self.corrector.connect(
            "new_spellcheck_offender", on_new_spellcheck_offender)

        sequence = "carl"
        self.corrector.increase_ticket(sequence)
        self.corrector.increase_ticket(sequence)
        self.corrector.increase_ticket(sequence)

        on_new_spellcheck_offender.assert_called_once_with(
            self.corrector, sequence)
        eq_(self.spellchecker.add.called, False)
