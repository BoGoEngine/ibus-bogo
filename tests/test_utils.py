#-*- coding: utf-8
#
# IBus-BoGo - The Vietnamese IME for IBus
#
# Copyright (c) 2012- Long T. Dam <longdt90@gmail.com>,
#                     Trung Ngo <ndtrung4419@gmail.com>
#
# This file is part of IBus-BoGo Project
# IBus-BoGo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# IBus-BoGo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with IBus-BoGo. If not, see <http://www.gnu.org/licenses/>.

import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'engine')))

import unittest
from bogo.utils import *


class TestUtils(unittest.TestCase):
    def test_append_comps(self):
        self.assertEqual(append_comps(['','',''], 'a'), ['','a',''])
        self.assertEqual(append_comps(['','a',''], 'a'), ['','aa',''])
        self.assertEqual(append_comps(['b','',''], 'a'), ['b','a',''])
        self.assertEqual(append_comps(['b','',''], 'b'), ['bb','',''])
        self.assertEqual(append_comps(['b','a','c'], 'd'), ['b','a','cd'])
        
    def test_change_case(self):
        self.assertEqual(change_case('ơ', 1), 'Ơ')
        self.assertEqual(change_case('ư', 1), 'Ư')
        self.assertEqual(change_case('Ơ', 1), 'Ơ')
        self.assertEqual(change_case('Ư', 1), 'Ư')
        self.assertEqual(change_case('ơ', 0), 'ơ')
        self.assertEqual(change_case('ư', 0), 'ư')
        self.assertEqual(change_case('Ơ', 0), 'ơ')
        self.assertEqual(change_case('Ư', 0), 'ư')
if __name__ == '__main__':
    unittest.main()
