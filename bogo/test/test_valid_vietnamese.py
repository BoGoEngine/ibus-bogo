from bogo.valid_vietnamese import is_valid_combination
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
