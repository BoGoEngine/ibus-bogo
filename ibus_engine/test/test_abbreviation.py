from nose.tools import eq_
from ibus_engine.abbr import AbbreviationExpander
from gi.repository import GObject
import threading
import time


class TestAbbreviationExpander():

    def setup(self):
        self.abbr = AbbreviationExpander()

    def tear_down(self):
        # Delete the test file
        pass

    def test_no_rule(self):
        eq_(self.abbr.expand("lorem ipsum"), "lorem ipsum")

    def test_simple_rule(self):
        self.abbr.add_rule("a", "abc")
        eq_(self.abbr.expand("a"), "abc")

    def test_watch_file_content(self):
        test_file_path = "/tmp/test_rules.json"

        loop = GObject.MainLoop()

        def mainloop():
            self.abbr.watch_file(test_file_path)
            loop.run()

        threading.Thread(target=mainloop).start()

        time.sleep(2)
        with open(test_file_path, "w") as test_file:
            test_file.write('{"a" : "abc"}')

        time.sleep(2)

        try:
            eq_(self.abbr.expand("a"), "abc")
        finally:
            loop.quit()

        # Remove the test file
        # ...

    def test_auto_capitalization(self):
        self.abbr.add_rule("tm", "thay mat")

        eq_(self.abbr.expand("tm"), "thay mat")
        eq_(self.abbr.expand("Tm"), "Tm")
        eq_(self.abbr.expand("TM"), "TM")

        self.abbr.config["auto-capitalize-expansion"] = True

        eq_(self.abbr.expand("tm"), "thay mat")
        eq_(self.abbr.expand("Tm"), "Thay mat")
        eq_(self.abbr.expand("TM"), "THAY MAT")
