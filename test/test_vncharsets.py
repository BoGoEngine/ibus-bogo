import vncharsets
from nose.tools import eq_
import os

vncharsets.init()


def _gp(path):
    """
    Good path. Returns an absolute path from the relative path.
    """
    return os.path.join(os.path.dirname(__file__), path)


def test_encode_string():
    eq_("tưởng niệm".encode("tcvn3"), b"t\xAD\xEBng ni\xD6m")


def test_decode_string():
    utf8 = open(_gp('CONTRIBUTE.utf-8')).read()
    with open(_gp('CONTRIBUTE.tcvn3')) as f:
    	tcvn3 = f.buffer.read()

    eq_(b"t\xAD\xEBng ni\xD6m".decode("tcvn3"), "tưởng niệm")
    eq_("em bò ñieân, xin ñöøng ñaùnh em".encode('latin-1').decode('vni'), "em bị điên, xin đừng đánh em")

    eq_(open(_gp('CONTRIBUTE.tcvn3'), encoding="tcvn3").read(), utf8)
    eq_(open(_gp('CONTRIBUTE.vni-win'), encoding="vni").read(), utf8)
    eq_(utf8.encode("tcvn3"), tcvn3)
