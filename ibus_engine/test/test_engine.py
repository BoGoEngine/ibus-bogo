from nose.tools import eq_
from gi.repository import IBus
from ibus_engine.ibus_engine import Engine
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

        expander = AbbreviationExpander()

        self.eng = Engine(config, expander)

    def send_keys(self, input, engine):
        [self.send_key(character, engine) for character in input]
        return self

    def send_key(self, input, engine):
        engine.do_process_key_event(ord(input), 0, 16)
        engine.do_process_key_event(ord(input),
                                    0,
                                    IBus.ModifierType.RELEASE_MASK)

    def send_bksp(self, engine):
        engine.on_special_key_pressed(IBus.BackSpace)
        return self

    def send_return(self, engine):
        engine.on_return_pressed()
        return self

    def send_space(self, engine):
        engine.do_process_key_event(ord('a'), IBus.space, 16)
        return self

    def test_1_bug_117(self):
        """
        baa + bksp => {new_string: b, raw_string: b}
        """

        self.send_keys("baa", self.eng).send_bksp(self.eng)

        eq_(self.eng.new_string, 'b')
        eq_(self.eng.raw_string, 'b')

    def test_2_bug_117(self):
        """
        bana + bksp => {new_string: bâ, raw_string: baa}
        """

        self.send_keys("bana", self.eng).send_bksp(self.eng)

        eq_(self.eng.new_string, 'bâ')
        eq_(self.eng.raw_string, 'baa')

    def test_3_bug_117(self):
        """
        ba + bksp + a => {new_string: ba, raw_string: ba}
        """

        self.send_keys("ba", self.eng) \
            .send_bksp(self.eng).send_keys("a", self.eng)

        eq_(self.eng.new_string, 'ba')
        eq_(self.eng.raw_string, 'ba')

    def test_4_bug_117(self):
        """
        thuow + bksp => {new_string: thu, raw_string: thu}
        """

        self.send_keys("thuow", self.eng).send_bksp(self.eng)

        eq_(self.eng.new_string, 'thu')
        eq_(self.eng.raw_string, 'thu')

    def test_bug_123(self):
        """
        Should not raise IndexError when backspace is sent repeatedly
        """

        self.send_bksp(self.eng)
        self.send_bksp(self.eng)
        self.send_bksp(self.eng)
        self.send_bksp(self.eng)
