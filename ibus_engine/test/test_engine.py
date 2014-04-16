from nose.tools import eq_
from ibus_engine.base_backend import BaseBackend
from ibus_engine.abbr import AbbreviationExpander


class TestEngine():
    def setup(self):
        config = {
            "input-method": "telex",
            "output-charset": "utf-8",
            "skip-non-vietnamese": True,
            "auto-capitalize-abbreviations": False,
            "default-input-methods": {
                "telex": {
                    "a": "a^",
                    "o": "o^",
                    "e": "e^",
                    "w": ["u*", "o*", "a+", "<ư"],
                    "d": "d-",
                    "f": "\\",
                    "s": "/",
                    "r": "?",
                    "x": "~",
                    "j": ".",
                    "]": "<ư",
                    "[": "<ơ",
                    "}": "<Ư",
                    "{": "<Ơ"
                },
            }
        }

        self.eng = BaseBackend(
            config=config,
            abbr_expander=AbbreviationExpander(),
            auto_corrector=None)

    def send_keys(self, input, engine):
        [self.send_key(character, engine) for character in input]
        return self

    def send_key(self, input, engine):
        engine.process_key_event(ord(input), 0)

    def send_bksp(self, engine):
        engine.on_backspace_pressed()
        return self

    def send_space(self, engine):
        engine.on_space_pressed()
        return self

    def test_1_bug_117(self):
        """
        baa + bksp => {new_string: b, raw_string: b}
        """

        self.send_keys("baa", self.eng).send_bksp(self.eng)

        eq_(self.eng.editing_string, 'b')
        eq_(self.eng.raw_string, 'b')

    def test_2_bug_117(self):
        """
        bana + bksp => {new_string: bâ, raw_string: baa}
        """

        self.send_keys("bana", self.eng).send_bksp(self.eng)

        eq_(self.eng.editing_string, 'bâ')
        eq_(self.eng.raw_string, 'baa')

    def test_3_bug_117(self):
        """
        ba + bksp + a => {new_string: ba, raw_string: ba}
        """

        self.send_keys("ba", self.eng) \
            .send_bksp(self.eng).send_keys("a", self.eng)

        eq_(self.eng.editing_string, 'ba')
        eq_(self.eng.raw_string, 'ba')

    def test_4_bug_117(self):
        """
        thuow + bksp => {new_string: thu, raw_string: thu}
        """

        self.send_keys("thuow", self.eng).send_bksp(self.eng)

        eq_(self.eng.editing_string, 'thu')
        eq_(self.eng.raw_string, 'thu')

    def test_bug_123(self):
        """
        Should not raise IndexError when backspace is sent repeatedly
        """

        self.send_bksp(self.eng)
        self.send_bksp(self.eng)
        self.send_bksp(self.eng)
        self.send_bksp(self.eng)
