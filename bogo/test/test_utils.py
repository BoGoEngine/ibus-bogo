# -*- coding: utf-8 -*-

from nose.tools import eq_
from bogo.utils import *


def test_separate():
    eq_(separate(''), ['', '', ''])

    eq_(separate('a'), ['', 'a', ''])
    eq_(separate('b'), ['b', '', ''])

    eq_(separate('aa'), ['', 'aa', ''])
    eq_(separate('ae'), ['', 'ae', ''])

    eq_(separate('bb'), ['bb', '', ''])
    eq_(separate('bc'), ['bc', '', ''])

    eq_(separate('ba'), ['b', 'a', ''])
    eq_(separate('baa'), ['b', 'aa', ''])
    eq_(separate('bba'), ['bb', 'a', ''])
    eq_(separate('bbaa'), ['bb', 'aa', ''])

    eq_(separate('bac'), ['b', 'a', 'c'])
    eq_(separate('baac'), ['b', 'aa', 'c'])
    eq_(separate('bbac'), ['bb', 'a', 'c'])
    eq_(separate('bbaacc'), ['bb', 'aa', 'cc'])

    eq_(separate('baca'), ['bac', 'a', ''])
    eq_(separate('bacaa'), ['bac', 'aa', ''])
    eq_(separate('bacaacaeb'), ['bacaac', 'ae', 'b'])

    eq_(separate('long'), ['l', 'o', 'ng'])
    eq_(separate('HoA'), ['H', 'oA', ''])
    eq_(separate('TruoNg'), ['Tr', 'uo', 'Ng'])
    eq_(separate(u'QuyÊn'), ['Qu', u'yÊ', 'n'])
    eq_(separate(u'Trùng'), ['Tr', u'ù', 'ng'])
    eq_(separate(u'uông'), ['', u'uô', 'ng'])
    eq_(separate(u'giƯờng'), ['gi', u'Ườ', 'ng'])
    eq_(separate('gi'), ['g', 'i', ''])
    eq_(separate('aoe'), ['', 'aoe', ''])
    eq_(separate('uo'), ['', 'uo', ''])
    eq_(separate('uong'), ['', 'uo', 'ng'])
    eq_(separate(u'nhếch'), ['nh', u'ế', 'ch'])
    eq_(separate(u'ếch'), ['', u'ế', 'ch'])
    eq_(separate(u'xẻng'), ['x', u'ẻ', 'ng'])
    eq_(separate(u'xoáy'), ['x', u'oáy', ''])
    eq_(separate(u'quây'), ['qu', u'ây', ''])
