#
# IBus-Bogo - The Vietnamese IME for IBus
#
# Copyright (c) 2012- Long T. Dam <longdt90@gmail.com>,
#                     Trung Ngo <ndtrung4419@gmail.com>
#
# This file is part of IBus-BoGo Project
# IBus-Bogo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# IBus-BoGo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with IBus-BoGo.  If not, see <http://www.gnu.org/licenses/>.

from BoGoConfig import *
from ctypes import *
import Charset

BoGoCpp = cdll.LoadLibrary(bogo_library)

# Cpp functions declaration here
cpp_process_key = BoGoCpp.py_processKey
cpp_process_key.restype = c_char_p

# Python wrappers of cpp functions
def process_key(string, keyval):
    _string = c_char_p(string.encode("utf8"))
    _keyval = c_char(keyval.encode("utf8"))
    result = unicode(cpp_process_key(_string, _keyval), "utf8")
    return result

def utf8_to_tcvn3(string):
    return Charset.utf8_to_tcvn3(string)
