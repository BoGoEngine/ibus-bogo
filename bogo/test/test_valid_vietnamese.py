from bogo.validation import is_valid_string
from nose.tools import ok_
import os


def test_from_dict():
    # Not sure why these words end up in the dictionary?
    exception = {
        'ping',
        'xit',
        'têt',
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

    dic = open(os.path.join(os.path.dirname(__file__), 'sequences/vi.dic'))
    for line in dic:
        yield atomic, line.rstrip()


def test_c_ending():
    assert is_valid_string("éc", final_form=True)
    assert is_valid_string("ác", final_form=True)
    assert is_valid_string("úc", final_form=True)
    assert is_valid_string("óc", final_form=True)

    assert is_valid_string("thớc", final_form=True) is False
    assert is_valid_string("ic", final_form=True) is False


def test_ch_ending():
    # Good
    assert is_valid_string("ếch", final_form=True)
    assert is_valid_string("thách", final_form=True)
    assert is_valid_string("ích", final_form=True)
    assert is_valid_string("khuếch", final_form=True) is True
    assert is_valid_string("huỵch", final_form=True) is True
    assert is_valid_string("hoạch", final_form=True) is True

    # Wrong vowels
    assert is_valid_string("ech", final_form=True) is False
    assert is_valid_string("och", final_form=True) is False

    # Wrong tones
    assert is_valid_string("ềch", final_form=True) is False
    assert is_valid_string("thảch", final_form=True) is False
    assert is_valid_string("ĩch", final_form=True) is False
    assert is_valid_string("khuêch", final_form=True) is False
    assert is_valid_string("huỳch", final_form=True) is False
    assert is_valid_string("hoảch", final_form=True) is False


def test_ng_ending():
    assert is_valid_string("thing", final_form=True) is False
    assert is_valid_string("thinh", final_form=True) is True

    assert is_valid_string("thương", final_form=True) is True
    assert is_valid_string("thơng", final_form=True) is False


def test_nh_ending():
    assert is_valid_string("nhanh")
    assert is_valid_string("lênh")
    assert is_valid_string("huỳnh")
    assert is_valid_string("tỉnh")
    assert is_valid_string("hoành")
    assert is_valid_string("xuềnh")
    assert is_valid_string("quỳnh")

    assert is_valid_string("ỳnh") is False
    assert is_valid_string("nhănh") is False
    assert is_valid_string("nhânh") is False
    assert is_valid_string("nhenh") is False
    assert is_valid_string("nhơnh") is False
    assert is_valid_string("nhunh") is False
    assert is_valid_string("nhưnh") is False


def test_non_final():
    assert is_valid_string("thuyen", final_form=False)
    assert is_valid_string("thuyen", final_form=True) is False

    assert is_valid_string("thuyeen", final_form=False) is False
    assert is_valid_string("thuyeeng", final_form=False) is False

    assert is_valid_string("ảch", final_form=False) is True
    assert is_valid_string("ảch", final_form=True) is False

    assert is_valid_string("ưoi", final_form=False)
    assert is_valid_string("ưoi", final_form=True) is False


def test_single_consonant():
    assert is_valid_string("d")
    assert is_valid_string("b")
    assert is_valid_string("c")
    assert is_valid_string("kh")
    assert is_valid_string("ng")
    assert is_valid_string("đ")

    assert is_valid_string("đm") is False


def test_non_terminal_vowels():
    assert is_valid_string("bang")
    assert is_valid_string("baing") is False
