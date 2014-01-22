from bogo.valid_vietnamese import is_valid_combination, is_valid_string
from bogo.utils import separate

import os


def test_from_dict():
    """
    Comprehensive testing with a dictionary.
    """
    def atomic(word):
        try:
            assert is_valid_combination(separate(word))
        except AssertionError:
            if word == 'ping':
                pass
            else:
                raise

    dic = open(os.path.join(os.path.dirname(__file__), 'sequences/vi.dic'))
    for line in dic:
        yield atomic, line.rstrip()


def test_c_ending():
    assert is_valid_string("ec", final_form=True)
    assert is_valid_string("ac", final_form=True)
    assert is_valid_string("uc", final_form=True)
    assert is_valid_string("oc", final_form=True)
    assert is_valid_string("ơc", final_form=True)

    assert is_valid_string("ic", final_form=True) is False
    assert is_valid_string("ic", final_form=False) is True


def test_ch_ending():
    assert is_valid_string("ếch", final_form=True)
    assert is_valid_string("ách", final_form=True)
    assert is_valid_string("ích", final_form=True)

    assert is_valid_string("ech", final_form=True) is False
    assert is_valid_string("och", final_form=True) is False

    assert is_valid_string("ìch", final_form=True) is False
    assert is_valid_string("ãch", final_form=True) is False


def test_ng_ending():
    assert is_valid_string("thing", final_form=True) is False
    assert is_valid_string("thinh", final_form=True) is True

    assert is_valid_string("thương", final_form=True) is True
    assert is_valid_string("thơng", final_form=True) is False


def test_nh_ending():
    pass


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
