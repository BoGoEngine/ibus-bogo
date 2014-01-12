from nose.tools import eq_
from nose.plugins.attrib import attr
from ibus_engine.abbr import AbbreviationExpander
from gi.repository import GObject
import threading
import time
import os


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

    @attr('skip-travis')
    def test_watch_file_content(self):
        import tempfile

        f = tempfile.NamedTemporaryFile(mode="w")
        f.write('{}')
        f.file.flush()

        loop = GObject.MainLoop()

        def mainloop():
            self.abbr.watch_file(f.name)
            loop.run()

        threading.Thread(target=mainloop).start()

        time.sleep(2)

        f.file.seek(0)
        f.write('{"a" : "abc"}')
        f.file.flush()

        time.sleep(2)

        try:
            eq_(self.abbr.expand("a"), "abc")
        finally:
            loop.quit()

        f.close()

    def test_auto_capitalization(self):
        self.abbr.add_rule("tm", "thay mat")

        eq_(self.abbr.expand("tm"), "thay mat")
        eq_(self.abbr.expand("Tm"), "Tm")
        eq_(self.abbr.expand("TM"), "TM")

        self.abbr.config["auto-capitalize-expansion"] = True

        eq_(self.abbr.expand("tm"), "thay mat")
        eq_(self.abbr.expand("Tm"), "Thay mat")
        eq_(self.abbr.expand("TM"), "THAY MAT")

    def test_parseUnikeyRules(self):
        test =  '''\
DO NOT DELETE THIS LINE*** version=1 ***
kg:không
kgcd:Không Gian Cộng Đồng
vn:Việt Nam\
'''
        self.abbr.parseUnikeyRules(test)