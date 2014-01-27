# -*- coding: utf-8 -*-

from bogo.mark import *
from nose.tools import eq_


class TestGetMarkChar():
    def test_basic_latin(self):
        eq_(get_mark_char('a'), Mark.NONE)
        eq_(get_mark_char('e'), Mark.NONE)
        eq_(get_mark_char('i'), Mark.NONE)
        eq_(get_mark_char('o'), Mark.NONE)
        eq_(get_mark_char('u'), Mark.NONE)

        eq_(get_mark_char('b'), Mark.NONE)
        eq_(get_mark_char('c'), Mark.NONE)
        eq_(get_mark_char('d'), Mark.NONE)
        eq_(get_mark_char('e'), Mark.NONE)
        eq_(get_mark_char('f'), Mark.NONE)

    def test_without_accent(self):
        eq_(get_mark_char(u'â'), Mark.HAT)
        eq_(get_mark_char(u'ô'), Mark.HAT)
        eq_(get_mark_char(u'ơ'), Mark.HORN)
        eq_(get_mark_char(u'ư'), Mark.HORN)
        eq_(get_mark_char(u'ă'), Mark.BREVE)
        eq_(get_mark_char(u'đ'), Mark.BAR)

    def test_with_accent(self):
        def atomic(char, _mark):
            eq_(get_mark_char(char), _mark)

        for char in u"áàảãạéèẻẽẹíìỉĩịóòỏõọúùủũụ":
            yield atomic, char, Mark.NONE

        for char in u"ấầẩẫậốồổỗộ":
            yield atomic, char, Mark.HAT

        for char in u"ớờởỡợứừửữự":
            yield atomic, char, Mark.HORN

        for char in u"ắằẳẵặ":
            yield atomic, char, Mark.BREVE

        eq_(get_mark_char(u'đ'), Mark.BAR)


class TestAddMarkChar():

    def atomic(self, char, _mark, result):
        eq_(add_mark_char(char, _mark), result)

    def test_same(self):
        for char in "aoieubcdef":
            yield self.atomic, char, Mark.NONE, char

        for char in u"áàảãạéèẻẽẹíìỉĩịóòỏõọúùủũụ":
            yield self.atomic, char, Mark.NONE, char

        for char in u"ấầẩẫậốồổỗộ":
            yield self.atomic, char, Mark.HAT, char

        for char in u"ớờởỡợứừửữự":
            yield self.atomic, char, Mark.HORN, char

        for char in u"ắằẳẵặ":
            yield self.atomic, char, Mark.BREVE, char

        self.atomic(u'đ', Mark.BAR, u'đ')

    def test_add_to_none(self):
        tests = [
            ('a', Mark.HAT,   u'â'),
            ('a', Mark.BREVE, u'ă'),
            ('a', Mark.HORN,   'a'),
            ('a', Mark.BAR,    'a'),

            ('e', Mark.HAT,  u'ê'),
            ('e', Mark.BREVE, 'e'),
            ('e', Mark.HORN,  'e'),
            ('e', Mark.BAR,   'e'),

            ('i', Mark.HAT,   'i'),
            ('i', Mark.BREVE, 'i'),
            ('i', Mark.HORN,  'i'),
            ('i', Mark.BAR,   'i'),

            ('o', Mark.HAT,  u'ô'),
            ('o', Mark.BREVE, 'o'),
            ('o', Mark.HORN, u'ơ'),
            ('o', Mark.BAR,   'o'),

            ('u', Mark.HAT,   'u'),
            ('u', Mark.BREVE, 'u'),
            ('u', Mark.HORN, u'ư'),
            ('u', Mark.BAR,   'u'),
        ]

        for test in tests:
            yield (self.atomic,) + test

    def test_change_mark(self):
        tests = [
            (u'â', Mark.BREVE, u'ă'),
            (u'â', Mark.HORN,  u'â'),
            (u'â', Mark.BAR,   u'â'),

            (u'ă', Mark.HAT,  u'â'),
            (u'ă', Mark.HORN, u'ă'),
            (u'ă', Mark.BAR,  u'ă'),

            (u'ê', Mark.BREVE, u'ê'),
            (u'ê', Mark.HORN,  u'ê'),
            (u'ê', Mark.BAR,   u'ê'),

            (u'ô', Mark.BREVE, u'ô'),
            (u'ô', Mark.HORN,  u'ơ'),
            (u'ô', Mark.BAR,   u'ô'),

            (u'ơ', Mark.BREVE, u'ơ'),
            (u'ơ', Mark.HAT,   u'ô'),
            (u'ơ', Mark.BAR,   u'ơ'),

            (u'ư', Mark.BREVE, u'ư'),
            (u'ư', Mark.HAT,   u'ư'),
            (u'ư', Mark.BAR,   u'ư'),
        ]

        for test in tests:
            yield (self.atomic,) + test

    def test_add_none(self):
        tests = [
            (u'ă', 'a'),
            (u'â', 'a'),
            (u'ê', 'e'),
            (u'ô', 'o'),
            (u'ơ', 'o'),
            (u'ư', 'u'),
            (u'đ', 'd'),

            (u'ắấ', u'á'),
            (u'ằầ', u'à'),
            (u'ẳẩ', u'ả'),
            (u'ẵẫ', u'ã'),
            (u'ặậ', u'ạ'),

            (u'ế', u'é'),
        ]
        for test in tests:
            for subtest in test[0]:
                yield self.atomic, subtest, Mark.NONE, test[1]


class TestAddMark():

    def test_add_mark_at(self):
        eq_(add_mark_at('a', 0, Mark.HAT), u'â')
        eq_(add_mark_at('a', 0, Mark.HORN), 'a')
        eq_(add_mark_at('an', 1, Mark.BREVE), 'an')
        eq_(add_mark_at(u'đang', 0, Mark.NONE), 'dang')
        eq_(add_mark_at(u'bẢn', 1, Mark.HAT), u'bẨn')
        eq_(add_mark_at('gang', -1, Mark.HAT), 'gang')
        eq_(add_mark_at(u'phuô', 3, Mark.HORN), u'phuơ')
        eq_(add_mark_at('uod', 2, Mark.BAR), u'uođ')
        eq_(add_mark_at('D', 0, Mark.BAR), u'Đ')
        eq_(add_mark_at('e', 0, Mark.HAT), u'ê')

    def test_add_mark(self):
        eq_(add_mark(['d', 'uo', 'ng'], Mark.BAR), [u'đ', 'uo', 'ng'])
        eq_(add_mark(['d', 'uo', 'ng'], Mark.HORN), ['d', u'ươ', 'ng'])
        eq_(add_mark(['d', u'uô', 'ng'], Mark.HORN), ['d', u'ươ', 'ng'])
        eq_(add_mark(['d', u'Á', ''], Mark.HAT), ['d', u'Ấ', ''])
        eq_(add_mark(['d', '', ''], Mark.BAR), [u'đ', '', ''])
        eq_(add_mark(['D', 'uo', 'ng'], Mark.BAR), [u'Đ', 'uo', 'ng'])
        eq_(add_mark(['d', 'e', ''], Mark.HAT), ['d', u'ê', ''])
