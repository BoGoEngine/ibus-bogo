#-*- coding: utf-8
#
# IBus-BoGo - The Vietnamese IME for IBus
#
# Copyright (c) 2012- Long T. Dam <longdt90@gmail.com>,
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
from bogo.new_bogo_engine import *
from bogo.accent import *
from bogo.mark import *
from bogo.utils import *

def process_seq(orig, seq, im='simple-telex'):
    string = u'' + orig
    for i in range(len(seq)):
        string = process_key(string, seq[i], im)
    return string

class TestBoGoEngine(unittest.TestCase):
    def test_separate(self):
        self.assertEqual(separate(u''), [u'',u'',u''])
        self.assertEqual(separate(u'long'), [u'l',u'o',u'ng'])
        self.assertEqual(separate(u'HoA'), [u'H',u'oA',u''])
        self.assertEqual(separate(u'TruoNg'), [u'Tr',u'uo',u'Ng'])
        self.assertEqual(separate(u'QuyÊn'), [u'Qu',u'yÊ',u'n'])
        self.assertEqual(separate(u'Trùng'), [u'Tr',u'ù',u'ng'])
        self.assertEqual(separate(u'uông'), [u'',u'uô',u'ng'])
        self.assertEqual(separate(u'giƯờng'), [u'gi',u'Ườ',u'ng'])
        self.assertEqual(separate(u'gi'), [u'g',u'i',u''])
        self.assertEqual(separate(u'qu'), [u'qu',u'',u''])
        self.assertEqual(separate(u'd'), [u'd',u'',u''])
        self.assertEqual(separate(u'a'), [u'',u'a',u''])
        self.assertEqual(separate(u'aoe'), None)
        self.assertEqual(separate(u'nn'), None)
        self.assertEqual(separate(u'uo'), [u'',u'uo',u''])
        self.assertEqual(separate(u'uong'), [u'',u'uo',u'ng'])

    def test_add_accent_char(self):
        self.assertEqual(add_accent_char(u'a', Accent.GRAVE), u'à')
        self.assertEqual(add_accent_char(u'a', Accent.ACUTE), u'á')
        self.assertEqual(add_accent_char(u'A', Accent.ACUTE), u'Á')
        self.assertEqual(add_accent_char(u'Ò', Accent.HOOK), u'Ỏ')
        self.assertEqual(add_accent_char(u'ỵ', Accent.NONE), u'y')
        self.assertEqual(add_accent_char(u'ă', Accent.TIDLE), u'ẵ')
        self.assertEqual(add_accent_char(u'Ế', Accent.DOT), u'Ệ')

    def test_add_mark_char(self):
        self.assertEqual(add_mark_char(u'E', Mark.HAT), u'Ê')
        self.assertEqual(add_mark_char(u'a', Mark.HAT), u'â')
        self.assertEqual(add_mark_char(u'â', Mark.BREVE), u'ă')
        self.assertEqual(add_mark_char(u'd', Mark.BAR), u'đ')
        self.assertEqual(add_mark_char(u'D', Mark.BAR), u'Đ')
        self.assertEqual(add_mark_char(u'u', Mark.HORN), u'ư')
        self.assertEqual(add_mark_char(u'ù', Mark.HAT), u'ù')
        self.assertEqual(add_mark_char(u'Á', Mark.HAT), u'Ấ')
        self.assertEqual(add_mark_char(u'ắ', Mark.HAT), u'ấ')
        self.assertEqual(add_mark_char(u'ắ', Mark.NONE), u'á')
        self.assertEqual(add_mark_char(u'Ố', Mark.NONE), u'Ó')

    def test_add_accent(self):
        '''
Only the vowel part will be changed after the add_accent take places
'''
        self.assertEqual(add_accent([u'', u'ươ', u'n'], Accent.ACUTE)[1], u'ướ')
        self.assertEqual(add_accent([u'', u'ưƠ', u'n'], Accent.GRAVE)[1], u'ưỜ')
        self.assertEqual(add_accent([u'', u'uyÊ', u'n'], Accent.DOT)[1], u'uyỆ')
        self.assertEqual(add_accent([u'', u'Ua', u''], Accent.ACUTE)[1], u'Úa')
        self.assertEqual(add_accent([u'', u'i', u''], Accent.TIDLE)[1], u'ĩ')
        self.assertEqual(add_accent([u'', u'oa', u'n'], Accent.DOT)[1], u'oạ')
        self.assertEqual(add_accent([u'', u'óa', u'n'], Accent.NONE)[1], u'oa')

    def test_add_mark_at(self):
        self.assertEqual(add_mark_at(u'a', 0, Mark.HAT), u'â')
        self.assertEqual(add_mark_at(u'a', 0, Mark.HORN), u'a')
        self.assertEqual(add_mark_at(u'an', 1, Mark.BREVE), u'an')
        self.assertEqual(add_mark_at(u'đang', 0, Mark.NONE), u'dang')
        self.assertEqual(add_mark_at(u'bẢn', 1, Mark.HAT), u'bẨn')
        self.assertEqual(add_mark_at(u'gang', -1, Mark.HAT), u'gang')
        self.assertEqual(add_mark_at(u'phuô', 3, Mark.HORN), u'phuơ')
        self.assertEqual(add_mark_at(u'uod', 2, Mark.BAR), u'uođ')
        self.assertEqual(add_mark_at(u'D', 0, Mark.BAR), u'Đ')
        self.assertEqual(add_mark_at(u'e', 0, Mark.HAT), u'ê')

    def test_add_mark(self):
        self.assertEqual(add_mark([u'd', u'uo', u'ng'], Mark.BAR),
                         [u'đ', u'uo', u'ng'])
        self.assertEqual(add_mark([u'd', u'uo', u'ng'], Mark.HORN),
                         [u'd', u'ươ', u'ng'])
        self.assertEqual(add_mark([u'd', u'uô', u'ng'], Mark.HORN),
                         [u'd', u'ươ', u'ng'])
        self.assertEqual(add_mark([u'd', u'Á', u''], Mark.HAT),
                         [u'd', u'Ấ', u''])
        self.assertEqual(add_mark([u'd', u'', u''], Mark.BAR), [u'đ', u'', u''])
        self.assertEqual(add_mark([u'D', u'uo', u'ng'], Mark.BAR),
                         [u'Đ', u'uo', u'ng'])
        self.assertEqual(add_mark([u'd', u'e', u''], Mark.HAT),
                         [u'd', u'ê', u''])

    def test_transform(self):
        s = separate
        self.assertEqual(transform(s(u'uong'),'o*'), s(u'ương'))
        self.assertEqual(transform(s(u'duong'),'o*'), s(u'dương'))
        self.assertEqual(transform(s(u'uong'),'u*'), s(u'ương'))
        self.assertEqual(transform(s(u'uong'),'a+'), s(u'uong'))
        self.assertEqual(transform(s(u'a'),'a+'), s(u'ă'))
        self.assertEqual(transform(s(u'muong'),'o*'), s(u'mương'))
        self.assertEqual(transform(s(u'muo'),'o^'), s(u'muô'))
        self.assertEqual(transform(s(u'toa'),'/'), s(u'tóa'))
        self.assertEqual(transform(s(u'toan'),'/'), s(u'toán'))
        self.assertEqual(transform(s(u'toán'),'/'), s(u'toán'))
        self.assertEqual(transform(s(u'nguyÊt'),'.'), s(u'nguyỆt'))
        self.assertEqual(transform(s(u'gi'),'\\'), s(u'gì'))
        self.assertEqual(transform(s(u'quản'),'~'), s(u'quãn'))
        self.assertEqual(transform(s(u'mua'),'u*'), s(u'mưa'))
        #self.assertEqual(transform(s(u'nguyet'),u'<o'), s(u'nguyeto'))
        self.assertEqual(transform(s(u''),u'<ư'), s(u'ư'))
        self.assertEqual(transform(s(u''),u'a^'), s(u''))
        self.assertEqual(transform(s(u'd'),'d-'), s(u'đ'))
        self.assertEqual(transform(s(u'Duong'),'d-'), s(u'Đuong'))
        self.assertEqual(transform(s(u'qu'),'?'), s(u'qu'))
        self.assertEqual(transform(s(u'de'),'e^'), s(u'dê'))
        self.assertEqual(transform(s(u'mơi'),'/'), s(u'mới'))
        self.assertEqual(transform(s(u'a'),'+o'), s(u'ao'))
        self.assertEqual(transform(s(u'an'),'+o'), ['', 'a', 'no'])
        self.assertEqual(transform([u'nn', '', ''],'+n'), [u'nnn', '', ''])
        self.assertEqual(transform([u'c', 'o', ''],'+n'), [u'c', 'o', 'n'])
        self.assertEqual(transform([u'c', 'o', ''],'+o'), [u'c', 'oo', ''])
        self.assertEqual(transform([u't', u'óa', ''],'+n'), [u't', u'oá', 'n'])
        self.assertEqual(transform([u't', u'óa', ''],'+o'), [u't', u'oáo', ''])
        

    def test_process_key(self):
        self.assertEqual(process_key(u'','v'), u'v')
        self.assertEqual(process_key(u'','w'), u'w')
        self.assertEqual(process_key(u'a','w'), u'ă')
        self.assertEqual(process_key(u'o','o'), u'ô')
        self.assertEqual(process_key(u'O','o'), u'Ô')
        self.assertEqual(process_key(u'd','d'), u'đ')
        self.assertEqual(process_key(u'mua','f'), u'mùa')
        self.assertEqual(process_key(u'Dông','d'), u'Đông')
        self.assertEqual(process_key(u'gi','f'), u'gì')
        self.assertEqual(process_key(u'loAn','j'), u'loẠn')
        self.assertEqual(process_key(u'muong','w'), u'mương')
        self.assertEqual(process_key(u'qu','r'), u'qur')
        self.assertEqual(process_key(u'Lổng','r'), u'Lôngr')
        self.assertEqual(process_key(u'LỔng','r'), u'LÔngr')
        self.assertEqual(process_key(u'Đông','d'), u'Dôngd')
        self.assertEqual(process_key(u'Đ','d'), u'Dd')
        self.assertEqual(process_key(u'Đương','d'), u'Dươngd')
        self.assertEqual(process_key(u'Dương','w'), u'Duongw')
        self.assertEqual(process_key(u'Tóa','n'), u'Toán')
        self.assertEqual(process_key(u'tún','w'), u'tứn')
        self.assertEqual(process_key(u'de','e'), u'dê')
        self.assertEqual(process_key(u'mơi','s'), u'mới')
        self.assertEqual(process_key(u'ư','a'), u'ưa')
        self.assertEqual(process_key(u'ư','o'), u'ưo')
        self.assertEqual(process_key(u'ư','w'), u'uw')
        self.assertEqual(process_key(u'đ','x'), u'đx')
        self.assertEqual(process_key(u'hoac','w'), u'hoăc')
        self.assertEqual(process_key(u'cuô','i'), u'cuôi')

    def test_process_seq(self):
        self.assertEqual(process_seq('', 'tooi'), u'tôi')
        self.assertEqual(process_seq('', 'chuyeenr'), u'chuyển')
        self.assertEqual(process_seq('', 'ddoonjg'), u'động')
        
        # Test fallback IM
        self.assertEqual(process_seq('', 'tooi', 'shut'), u'tôi')
        self.assertEqual(process_seq('', 'chuyeenr', 'down'), u'chuyển')
        self.assertEqual(process_seq('', 'ddoonjg', 'blah'), u'động')
        
if __name__ == '__main__':
    unittest.main()
