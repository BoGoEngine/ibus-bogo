from bogo.valid_vietnamese import is_valid_combination, is_valid_string
from bogo.utils import separate

import os


def test_from_dict():
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
