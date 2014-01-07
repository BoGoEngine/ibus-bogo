from nose.tools import eq_
from ibus_engine.abbr import AbbreviationExpander
from gi.repository import GObject
import threading


class TestAbbreviationExpander():

    def setup(self):
        self.test_file_path = "/tmp/test_abbr.json"
        with open(self.test_file_path, "w") as test_file:
            pass
            test_file.write("{}")

        self.config = {
            "abbreviation-rules-path": self.test_file_path,
            "auto-capitalize-abbreviations": False
        }
        self.abbr = AbbreviationExpander(self.config)

    def tear_down(self):
        # Delete the test file
        pass

    def test_empty_file(self):
        eq_(self.abbr.expand("lorem ipsum"), "lorem ipsum")

    def test_watch_file_content(self):
        loop = GObject.MainLoop()

        def mainloop():
            loop.run()

        threading.Thread(target=mainloop).start()

        test_file = open(self.test_file_path, "w")
        test_file.write('{"a" : "abc"}')
        test_file.close()

        import time
        time.sleep(2)

        try:
            eq_(self.abbr.expand("a"), "abc")
        finally:
            loop.quit()

    def test_auto_capitalization(self):
        test_file = open(self.test_file_path, "w")
        test_file.write('{"tm" : "thay mat"}')
        test_file.close()

        self.abbr.parse_abbr_rule()

        eq_(self.abbr.expand("tm"), "thay mat")
        eq_(self.abbr.expand("Tm"), "Tm")
        eq_(self.abbr.expand("TM"), "TM")

        self.config["auto-capitalize-abbreviations"] = True

        eq_(self.abbr.expand("tm"), "thay mat")
        eq_(self.abbr.expand("Tm"), "Thay mat")
        eq_(self.abbr.expand("TM"), "THAY MAT")
