from nose.tools import eq_, raises
from gi.repository import IBus
from ibus_engine.ibus_engine import Engine


class TestEngine():
    def send_keys(self, input, engine):
        [self.send_key(character, engine) for character in input]
        return self

    def send_key(self, input, engine):
        engine.do_process_key_event(ord(input), 0, 16)
        engine.do_process_key_event(ord(input),
                                    0,
                                    IBus.ModifierType.RELEASE_MASK)

    def send_bksp(self, engine):
        engine.on_backspace_pressed()
        return self

    def test_1_bug_117(self):
        """
        baa + bksp => {new_string: b, raw_string: b}
        """
        eng = Engine()

        self.send_keys("baa", eng).send_bksp(eng)

        eq_(eng.new_string, 'b')
        eq_(eng._Engine__raw_string, 'b')

    def test_2_bug_117(self):
        """
        bana + bksp => {new_string: bâ, raw_string: baa}
        """
        eng = Engine()

        self.send_keys("bana", eng).send_bksp(eng)

        eq_(eng.new_string, 'bâ')
        eq_(eng._Engine__raw_string, 'baa')

    def test_3_bug_117(self):
        """
        ba + bksp + a => {new_string: ba, raw_string: ba}
        """
        eng = Engine()

        self.send_keys("ba", eng).send_bksp(eng).send_keys("a", eng)

        eq_(eng.new_string, 'ba')
        eq_(eng._Engine__raw_string, 'ba')

    def test_4_bug_117(self):
        """
        thuow + bksp => {new_string: thu, raw_string: thu}
        """
        eng = Engine()

        self.send_keys("thuow", eng).send_bksp(eng)

        eq_(eng.new_string, 'thu')
        eq_(eng._Engine__raw_string, 'thu')

    def test_bug_123(self):
        """
        Should not raise IndexError when backspace is sent repeatedly
        """
        eng = Engine()

        self.send_bksp(eng)
        self.send_bksp(eng)
        self.send_bksp(eng)
        self.send_bksp(eng)
