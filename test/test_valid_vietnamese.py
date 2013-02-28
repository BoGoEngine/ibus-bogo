from bogo.valid_vietnamese import is_valid_combination
from bogo.new_bogo_engine import separate
from nose.tools import eq_, ok_

import os

def test_from_dict():
	def atomic(word):
		assert is_valid_combination(separate(word))

	dic = open(os.path.join(os.path.dirname(__file__), 'vi.dic'))
	for line in dic:
		yield atomic, line.rstrip()