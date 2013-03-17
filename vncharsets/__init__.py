import codecs
from . import tcvn3, vni

"""
Register Vietnamese-specific decode-encoders into Python's codecs
infrastructure. All you have to do to read a tcvn3-encoded file for example
should be as simple as:
	
	import vncharsets

	with open('my_file.txt', encoding='tcvn3') as f:
		print(f.read())

The file's content will be converted to utf-8 (and vice-versa) on-the-fly.

Currently, this package supports 'vni' and 'tcvn3' codecs.
"""

initialized = False

def search_function(encoding_name):
	# TODO automatic
	if encoding_name == "vni":
		return vni.getregentry()
	if encoding_name == "tcvn3":
		return tcvn3.getregentry()

def init():
	global initialized
	if not initialized:
		codecs.register(search_function)
		initialized = True
