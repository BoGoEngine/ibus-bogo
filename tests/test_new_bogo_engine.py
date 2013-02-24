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
import copy
from bogo.new_bogo_engine import *
from bogo.accent import *
from bogo.mark import *
from bogo.utils import *

telex = default_config.copy()

def process_seq(orig, seq, config = telex):
    string = orig
    raw = string
    for i in seq:
        raw = raw + i
        string = process_key(string, i, raw_string = raw, config = telex)
    return string

class TestBoGoEngine(unittest.TestCase):
    def test_separate(self):
        self.assertEqual(separate(''), ['','',''])
        self.assertEqual(separate('long'), ['l','o','ng'])
        self.assertEqual(separate('HoA'), ['H','oA',''])
        self.assertEqual(separate('TruoNg'), ['Tr','uo','Ng'])
        self.assertEqual(separate('QuyÊn'), ['Qu','yÊ','n'])
        self.assertEqual(separate('Trùng'), ['Tr','ù','ng'])
        self.assertEqual(separate('uông'), ['','uô','ng'])
        self.assertEqual(separate('giƯờng'), ['gi','Ườ','ng'])
        self.assertEqual(separate('gi'), ['g','i',''])
        self.assertEqual(separate('q'), ['q','',''])
        self.assertEqual(separate('d'), ['d','',''])
        self.assertEqual(separate('a'), ['','a',''])
        self.assertEqual(separate('aoe'), ['', 'aoe', ''])
        #self.assertEqual(separate('nn'), None)
        self.assertEqual(separate('uo'), ['','uo',''])
        self.assertEqual(separate('uong'), ['','uo','ng'])
        self.assertEqual(separate('nhếch'), ['nh','ế','ch'])
        self.assertEqual(separate('ếch'), ['','ế','ch'])
        self.assertEqual(separate('xẻng'), ['x','ẻ','ng'])
        self.assertEqual(separate('xoáy'), ['x','oáy',''])
        self.assertEqual(separate('quây'), ['qu','ây',''])

        self.assertEqual(separate('a'), ['','a',''])
        self.assertEqual(separate('b'), ['b','',''])
        
        self.assertEqual(separate('aa'), ['','aa',''])
        self.assertEqual(separate('ae'), ['','ae',''])

        self.assertEqual(separate('bb'), ['bb','',''])
        self.assertEqual(separate('bc'), ['bc','',''])

        self.assertEqual(separate('ba'), ['b','a',''])
        self.assertEqual(separate('baa'), ['b','aa',''])
        self.assertEqual(separate('bba'), ['bb','a',''])
        self.assertEqual(separate('bbaa'), ['bb','aa',''])

        self.assertEqual(separate('bac'), ['b','a','c'])
        self.assertEqual(separate('baac'), ['b','aa','c'])
        self.assertEqual(separate('bbac'), ['bb','a','c'])
        self.assertEqual(separate('bbaacc'), ['bb','aa','cc'])

        self.assertEqual(separate('baca'), ['bac','a',''])
        self.assertEqual(separate('bacaa'), ['bac','aa',''])
        self.assertEqual(separate('bacaacaeb'), ['bacaac','ae','b'])



    def test_valid_vietnamese(self):
        self.assertEqual(is_valid_combination(['c', 'a', 'se']), False)

    def test_add_accent_char(self):
        self.assertEqual(add_accent_char('a', Accent.GRAVE), 'à')
        self.assertEqual(add_accent_char('a', Accent.ACUTE), 'á')
        self.assertEqual(add_accent_char('A', Accent.ACUTE), 'Á')
        self.assertEqual(add_accent_char('Ò', Accent.HOOK), 'Ỏ')
        self.assertEqual(add_accent_char('ỵ', Accent.NONE), 'y')
        self.assertEqual(add_accent_char('ă', Accent.TIDLE), 'ẵ')
        self.assertEqual(add_accent_char('Ế', Accent.DOT), 'Ệ')

    def test_add_mark_char(self):
        self.assertEqual(add_mark_char('E', Mark.HAT), 'Ê')
        self.assertEqual(add_mark_char('a', Mark.HAT), 'â')
        self.assertEqual(add_mark_char('â', Mark.BREVE), 'ă')
        self.assertEqual(add_mark_char('d', Mark.BAR), 'đ')
        self.assertEqual(add_mark_char('D', Mark.BAR), 'Đ')
        self.assertEqual(add_mark_char('u', Mark.HORN), 'ư')
        self.assertEqual(add_mark_char('ù', Mark.HAT), 'ù')
        self.assertEqual(add_mark_char('Á', Mark.HAT), 'Ấ')
        self.assertEqual(add_mark_char('ắ', Mark.HAT), 'ấ')
        self.assertEqual(add_mark_char('ắ', Mark.NONE), 'á')
        self.assertEqual(add_mark_char('Ố', Mark.NONE), 'Ó')

    def test_add_accent(self):
        '''
Only the vowel part will be changed after the add_accent take places
'''
        self.assertEqual(add_accent(['', 'ươ', 'n'], Accent.ACUTE)[1], 'ướ')
        self.assertEqual(add_accent(['', 'ưƠ', 'n'], Accent.GRAVE)[1], 'ưỜ')
        self.assertEqual(add_accent(['', 'uyÊ', 'n'], Accent.DOT)[1], 'uyỆ')
        self.assertEqual(add_accent(['', 'Ua', ''], Accent.ACUTE)[1], 'Úa')
        self.assertEqual(add_accent(['', 'i', ''], Accent.TIDLE)[1], 'ĩ')
        self.assertEqual(add_accent(['', 'oa', 'n'], Accent.DOT)[1], 'oạ')
        self.assertEqual(add_accent(['', 'óa', 'n'], Accent.NONE)[1], 'oa')

    def test_add_mark_at(self):
        self.assertEqual(add_mark_at('a', 0, Mark.HAT), 'â')
        self.assertEqual(add_mark_at('a', 0, Mark.HORN), 'a')
        self.assertEqual(add_mark_at('an', 1, Mark.BREVE), 'an')
        self.assertEqual(add_mark_at('đang', 0, Mark.NONE), 'dang')
        self.assertEqual(add_mark_at('bẢn', 1, Mark.HAT), 'bẨn')
        self.assertEqual(add_mark_at('gang', -1, Mark.HAT), 'gang')
        self.assertEqual(add_mark_at('phuô', 3, Mark.HORN), 'phuơ')
        self.assertEqual(add_mark_at('uod', 2, Mark.BAR), 'uođ')
        self.assertEqual(add_mark_at('D', 0, Mark.BAR), 'Đ')
        self.assertEqual(add_mark_at('e', 0, Mark.HAT), 'ê')

    def test_add_mark(self):
        self.assertEqual(add_mark(['d', 'uo', 'ng'], Mark.BAR),
                         ['đ', 'uo', 'ng'])
        self.assertEqual(add_mark(['d', 'uo', 'ng'], Mark.HORN),
                         ['d', 'ươ', 'ng'])
        self.assertEqual(add_mark(['d', 'uô', 'ng'], Mark.HORN),
                         ['d', 'ươ', 'ng'])
        self.assertEqual(add_mark(['d', 'Á', ''], Mark.HAT),
                         ['d', 'Ấ', ''])
        self.assertEqual(add_mark(['d', '', ''], Mark.BAR), ['đ', '', ''])
        self.assertEqual(add_mark(['D', 'uo', 'ng'], Mark.BAR),
                         ['Đ', 'uo', 'ng'])
        self.assertEqual(add_mark(['d', 'e', ''], Mark.HAT),
                         ['d', 'ê', ''])

    def test_transform(self):
        s = separate
        self.assertEqual(transform(s('uong'),'o*'), s('ương'))
        self.assertEqual(transform(s('duong'),'o*'), s('dương'))
        self.assertEqual(transform(s('uong'),'u*'), s('ương'))
        self.assertEqual(transform(s('uong'),'a+'), s('uong'))
        self.assertEqual(transform(s('a'),'a+'), s('ă'))
        self.assertEqual(transform(s('muong'),'o*'), s('mương'))
        self.assertEqual(transform(s('muo'),'o^'), s('muô'))
        self.assertEqual(transform(s('toa'),'/'), s('tóa'))
        self.assertEqual(transform(s('toan'),'/'), s('toán'))
        self.assertEqual(transform(s('toán'),'/'), s('toán'))
        self.assertEqual(transform(s('nguyÊt'),'.'), s('nguyỆt'))
        self.assertEqual(transform(s('gi'),'\\'), s('gì'))
        self.assertEqual(transform(s('quản'),'~'), s('quãn'))
        self.assertEqual(transform(s('mua'),'u*'), s('mưa'))
        #self.assertEqual(transform(s('nguyet'),'<o'), s('nguyeto'))
        self.assertEqual(transform(s(''),'<ư'), s('ư'))
        self.assertEqual(transform(s(''),'a^'), s(''))
        #self.assertEqual(transform(s('d'),'d-'), s('đ'))
        self.assertEqual(transform(s('Duong'),'d-'), s('Đuong'))
        self.assertEqual(transform(s('q'),'?'), s('q'))
        self.assertEqual(transform(s('de'),'e^'), s('dê'))
        self.assertEqual(transform(s('mơi'),'/'), s('mới'))
        self.assertEqual(transform(s('a'),'+o'), s('ao'))
        self.assertEqual(transform(s('an'),'+o'), ['', 'a', 'no'])
        self.assertEqual(transform(['nn', '', ''],'+n'), ['nnn', '', ''])
        self.assertEqual(transform(['c', 'o', ''],'+n'), ['c', 'o', 'n'])
        self.assertEqual(transform(['c', 'o', ''],'+o'), ['c', 'oo', ''])
        self.assertEqual(transform(['t', 'óa', ''],'+n'), ['t', 'oá', 'n'])
        self.assertEqual(transform(['t', 'óa', ''],'+o'), ['t', 'oáo', ''])
        self.assertEqual(transform(['', 'u', ''], 'u*'), ['', 'ư', ''])
        self.assertEqual(transform(['','Ư', ''], '<Ư'), ['','Ư', ''])
        

    def test_process_key(self):
        self.assertEqual(process_key('','v'), 'v')
        self.assertEqual(process_key('a','w'), 'ă')
        self.assertEqual(process_key('','w'), 'ư')
        self.assertEqual(process_key('o','w'), 'ơ')
        self.assertEqual(process_key('o','o'), 'ô')
        self.assertEqual(process_key('O','o'), 'Ô')
        self.assertEqual(process_key('d','d'), 'đ')
        self.assertEqual(process_key('','w', config = telex), 'ư')
        self.assertEqual(process_key('mua','f'), 'mùa')
        self.assertEqual(process_key('Dông','d'), 'Đông')
        self.assertEqual(process_key('gi','f'), 'gì')
        self.assertEqual(process_key('loAn','j'), 'loẠn')
        self.assertEqual(process_key('muong','w'), 'mương')
        self.assertEqual(process_key('qu','r'), 'qur')
        self.assertEqual(process_key('Lổng','r'), 'Lôngr')
        self.assertEqual(process_key('LỔng','r'), 'LÔngr')
        self.assertEqual(process_key('Đông','d'), 'Dôngd')
        self.assertEqual(process_key('Đ','d'), 'Dd')
        self.assertEqual(process_key('Đương','d'), 'Dươngd')
        self.assertEqual(process_key('Dương','w'), 'Duongw')
        self.assertEqual(process_key('Tóa','n'), 'Toán')
        self.assertEqual(process_key('tún','w'), 'tứn')
        self.assertEqual(process_key('de','e'), 'dê')
        self.assertEqual(process_key('mơi','s'), 'mới')
        self.assertEqual(process_key('ư','a'), 'ưa')
        self.assertEqual(process_key('ư','o'), 'ưo')
        self.assertEqual(process_key('ư','w'), 'uw')
        self.assertEqual(process_key('đ','x'), 'đx')
        self.assertEqual(process_key('hoac','w'), 'hoăc')
        self.assertEqual(process_key('cuô','i'), 'cuôi')
        self.assertEqual(process_key('cá','e'), 'cáe')
        self.assertEqual(process_key('',']', config = telex, case=1), 'Ư')
        self.assertEqual(process_key('','[', config = telex, case=1), 'Ơ')
        self.assertEqual(process_key('i','w', config = telex), 'iw')
        
        # Undo
        self.assertEqual(process_key('â','a'), 'aa')
        self.assertEqual(process_key('ă','w'), 'aw')
        self.assertEqual(process_key('á','s'), 'as')
        self.assertEqual(process_key('à','f'), 'af')
        self.assertEqual(process_key('ả','r'), 'ar')
        self.assertEqual(process_key('ã','x'), 'ax')
        self.assertEqual(process_key('ạ','j'), 'aj')
        self.assertEqual(process_key('ư','w'), 'uw')
        self.assertEqual(process_key('ơ','w'), 'ow')
        self.assertEqual(process_key('ư',']', config = telex), ']')
        self.assertEqual(process_key('ơ','[', config = telex), '[')
        self.assertEqual(process_key('Ư',']', config = telex, case=1), ']')
        self.assertEqual(process_key('Ơ','[', config = telex, case=1), '[')
        self.assertEqual(process_key('ư','}', config = telex), '}') # Programmer Dvorak
        self.assertEqual(process_key('ơ','{', config = telex), '{')
        self.assertEqual(process_key('Ư','}', config = telex, case=1), '}')
        self.assertEqual(process_key('Ơ','{', config = telex, case=1), '{')
        self.assertEqual(process_key('hư','w', config = telex, case=1), 'huw')
        
        # Undo with 'z'
        self.assertEqual(process_key('â','z'), 'a')
        self.assertEqual(process_key('ă','z'), 'a')
        self.assertEqual(process_key('ê','z'), 'e')
        self.assertEqual(process_key('ơ','z'), 'o')
        self.assertEqual(process_key('ô','z'), 'o')
        self.assertEqual(process_key('ư','z'), 'u')
        
        self.assertEqual(process_key('ấ','z'), 'â')
        self.assertEqual(process_key('ẩ','z'), 'â')
        self.assertEqual(process_key('ậ','z'), 'â')
        
                
        # Abbreviations
        #self.assertEqual(process_key('đ','m'), 'đm')
        #self.assertEqual(process_key('đ','c'), 'đc')
        #self.assertEqual(process_key('kgcd','d'), 'kgcđ')

    def test_process_seq(self):
        self.assertEqual(process_seq('', 'tooi'), 'tôi')
        self.assertEqual(process_seq('', 'chuyeenr'), 'chuyển')
        self.assertEqual(process_seq('', 'ddoonjg'), 'động')
        self.assertEqual(process_seq('nhê', 'chs'), 'nhếch')
        
        # Test fallback IM
        self.assertEqual(process_seq('', 'tooi', 'shut'), 'tôi')
        self.assertEqual(process_seq('', 'chuyeenr', 'down'), 'chuyển')
        self.assertEqual(process_seq('', 'ddoonjg', 'blah'), 'động')

        # Test Undo
        self.assertEqual(process_seq('h', 'uww'), 'huw')
        self.assertEqual(process_seq('h', 'ww'), 'hw')
        self.assertEqual(process_seq('', 'ww'), 'w')
        self.assertEqual(process_seq('', 'uww'), 'uw')
        
if __name__ == '__main__':
    unittest.main()
