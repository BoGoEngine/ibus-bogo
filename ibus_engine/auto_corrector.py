from gi.repository import GObject
from collections import defaultdict
import bogo


class AutoCorrector(GObject.Object):

    __gsignals__ = {
        'new_spellcheck_offender': (GObject.SIGNAL_RUN_LAST, bool,
                                    (str,))
    }

    def __init__(self, config, spellchecker, english_spellchecker):
        self.config = config
        self.spellchecker = spellchecker
        self.english_spellchecker = english_spellchecker
        self.offence_tickets = defaultdict(lambda: 0)
        super().__init__()

    # http://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
    def levenshtein(self, s1, s2):
        if len(s1) < len(s2):
            return self.levenshtein(s2, s1)

        # len(s1) >= len(s2)
        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
                deletions = current_row[j] + 1       # than s2
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def suggest(self, key_sequence):
        """
        Try to suggest a key sequence that evaluates to a correct
        Vietnamese word. May return the exact input if that key
        sequence is blacklisted or if there is no suggestion.
        """
        if self.spellchecker.check(key_sequence):
            # This key sequence is blacklisted
            return key_sequence

        try:
            suggested = self.spellchecker.suggest(key_sequence)[0]
            max_distance = \
                self.config["typo-correction-level"]
            distance = self.levenshtein(key_sequence, suggested)

            # Double check with the English spellchecker so that
            # we don't auto-correct short and correct English words
            if not self.english_spellchecker.check(key_sequence) and \
                    distance <= max_distance:
                return ' '.join(map(self.process_seq,
                                suggested.split(' ')))
        except IndexError:
            # No suggestion is found
            return key_sequence

    def increase_ticket(self, key_sequence):
        self.offence_tickets[key_sequence] += 1

        if self.offence_tickets[key_sequence] == 3:
            if self.emit(
                    'new_spellcheck_offender',
                    key_sequence):
                self.spellchecker.add(key_sequence)
            else:
                self.offence_tickets[key_sequence] = 0

    def process_seq(self, seq):
        string = ""
        raw = string
        for i in seq:
            string, raw = bogo.process_key(string,
                                           i,
                                           fallback_sequence=raw,
                                           config=self.config)
        return string
