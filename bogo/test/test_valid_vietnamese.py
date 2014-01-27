# -*- coding: utf-8 -*-

from bogo.validation import is_valid_string
from nose.tools import ok_
import os
import codecs


def test_from_dict():
    # Not sure why these words end up in the dictionary?
    exception = {
        'ping',
        'xit',
        u'têt',
        'gip'
    }

    def atomic(word):
        try:
            ok_(is_valid_string(word))
        except AssertionError:
            if word in exception:
                pass
            else:
                raise

    dic = codecs.open(os.path.join(os.path.dirname(__file__),
                                   'sequences/vi.dic'),
                      encoding="utf-8")
    for line in dic:
        yield atomic, line.rstrip()


def test_c_ending():
    assert is_valid_string(u"éc", final_form=True)
    assert is_valid_string(u"ác", final_form=True)
    assert is_valid_string(u"úc", final_form=True)
    assert is_valid_string(u"óc", final_form=True)

    assert is_valid_string(u"thớc", final_form=True) is False
    assert is_valid_string("ic", final_form=True) is False


def test_ch_ending():
    # Good
    assert is_valid_string(u"ếch", final_form=True)
    assert is_valid_string(u"thách", final_form=True)
    assert is_valid_string(u"ích", final_form=True)
    assert is_valid_string(u"khuếch", final_form=True) is True
    assert is_valid_string(u"huỵch", final_form=True) is True
    assert is_valid_string(u"hoạch", final_form=True) is True

    # Wrong vowels
    assert is_valid_string("ech", final_form=True) is False
    assert is_valid_string("och", final_form=True) is False

    # Wrong tones
    assert is_valid_string(u"ềch", final_form=True) is False
    assert is_valid_string(u"thảch", final_form=True) is False
    assert is_valid_string(u"ĩch", final_form=True) is False
    assert is_valid_string(u"khuêch", final_form=True) is False
    assert is_valid_string(u"huỳch", final_form=True) is False
    assert is_valid_string(u"hoảch", final_form=True) is False


# def test_ng_ending():
#     assert is_valid_string("thing", final_form=True) is False
#     assert is_valid_string("thinh", final_form=True) is True

#     assert is_valid_string("thương", final_form=True) is True
#     assert is_valid_string("thơng", final_form=True) is False


# def test_nh_ending():
#     assert is_valid_string("nhanh")
#     assert is_valid_string("lênh")
#     assert is_valid_string("huỳnh")
#     assert is_valid_string("tỉnh")
#     assert is_valid_string("hoành")
#     assert is_valid_string("xuềnh")
#     assert is_valid_string("quỳnh")

#     assert is_valid_string("ỳnh") is False
#     assert is_valid_string("nhănh") is False
#     assert is_valid_string("nhânh") is False
#     assert is_valid_string("nhenh") is False
#     assert is_valid_string("nhơnh") is False
#     assert is_valid_string("nhunh") is False
#     assert is_valid_string("nhưnh") is False


def test_non_final():
    assert is_valid_string("thuyen", final_form=False)
    assert is_valid_string("thuyen", final_form=True) is False

    assert is_valid_string("thuyeen", final_form=False) is False
    assert is_valid_string("thuyeeng", final_form=False) is False

    assert is_valid_string(u"ảch", final_form=False) is True
    assert is_valid_string(u"ảch", final_form=True) is False

    assert is_valid_string(u"ưoi", final_form=False)
    assert is_valid_string(u"ưoi", final_form=True) is False

    assert is_valid_string("aun", final_form=False) is False
    assert is_valid_string("uoin", final_form=False) is False


def test_single_consonant():
    assert is_valid_string("d")
    assert is_valid_string("b")
    assert is_valid_string("c")
    assert is_valid_string("kh")
    assert is_valid_string("ng")
    assert is_valid_string(u"đ")
    assert is_valid_string(u"đm")
    assert is_valid_string(u"đc")
    assert is_valid_string("kgcd")


def test_non_terminal_vowels():
    assert is_valid_string("bang")
    assert is_valid_string("baing") is False
