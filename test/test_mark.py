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
        eq_(get_mark_char('â'), Mark.HAT)
        eq_(get_mark_char('ô'), Mark.HAT)
        eq_(get_mark_char('ơ'), Mark.HORN)
        eq_(get_mark_char('ư'), Mark.HORN)
        eq_(get_mark_char('ă'), Mark.BREVE)
        eq_(get_mark_char('đ'), Mark.BAR)

    def test_with_accent(self):
        def atomic(char, _mark):
            eq_(get_mark_char(char), _mark)

        for char in "áàảãạéèẻẽẹíìỉĩịóòỏõọúùủũụ":
            yield atomic, char, Mark.NONE

        for char in "ấầẩẫậốồổỗộ":
            yield atomic, char, Mark.HAT

        for char in "ớờởỡợứừửữự":
            yield atomic, char, Mark.HORN

        for char in "ắằẳẵặ":
            yield atomic, char, Mark.BREVE

        eq_(get_mark_char('đ'), Mark.BAR)


class TestAddMarkChar():

    def atomic(self, char, _mark, result):
        eq_(add_mark_char(char, _mark), result)

    def test_same(self):
        for char in "aoieubcdef":
            yield self.atomic, char, Mark.NONE, char

        for char in "áàảãạéèẻẽẹíìỉĩịóòỏõọúùủũụ":
            yield self.atomic, char, Mark.NONE, char

        for char in "ấầẩẫậốồổỗộ":
            yield self.atomic, char, Mark.HAT, char

        for char in "ớờởỡợứừửữự":
            yield self.atomic, char, Mark.HORN, char

        for char in "ắằẳẵặ":
            yield self.atomic, char, Mark.BREVE, char

        self.atomic('đ', Mark.BAR, 'đ')

    def test_add_to_none(self):
        tests = [
            ('a', Mark.HAT, 'â'),
            ('a', Mark.BREVE, 'ă'),
            ('a', Mark.HORN, 'a'),
            ('a', Mark.BAR, 'a'),

            ('e', Mark.HAT, 'ê'),
            ('e', Mark.BREVE, 'e'),
            ('e', Mark.HORN, 'e'),
            ('e', Mark.BAR, 'e'),

            ('i', Mark.HAT, 'i'),
            ('i', Mark.BREVE, 'i'),
            ('i', Mark.HORN, 'i'),
            ('i', Mark.BAR, 'i'),

            ('o', Mark.HAT, 'ô'),
            ('o', Mark.BREVE, 'o'),
            ('o', Mark.HORN, 'ơ'),
            ('o', Mark.BAR, 'o'),

            ('u', Mark.HAT, 'u'),
            ('u', Mark.BREVE, 'u'),
            ('u', Mark.HORN, 'ư'),
            ('u', Mark.BAR, 'u'),
        ]

        for test in tests:
            yield (self.atomic,) + test

    def test_change_mark(self):
        tests = [
            ('â', Mark.BREVE, 'ă'),
            ('â', Mark.HORN, 'â'),
            ('â', Mark.BAR, 'â'),

            ('ă', Mark.HAT, 'â'),
            ('ă', Mark.HORN, 'ă'),
            ('ă', Mark.BAR, 'ă'),

            ('ê', Mark.BREVE, 'ê'),
            ('ê', Mark.HORN, 'ê'),
            ('ê', Mark.BAR, 'ê'),

            ('ô', Mark.BREVE, 'ô'),
            ('ô', Mark.HORN, 'ơ'),
            ('ô', Mark.BAR, 'ô'),

            ('ơ', Mark.BREVE, 'ơ'),
            ('ơ', Mark.HAT, 'ô'),
            ('ơ', Mark.BAR, 'ơ'),

            ('ư', Mark.BREVE, 'ư'),
            ('ư', Mark.HAT, 'ư'),
            ('ư', Mark.BAR, 'ư'),
        ]

        for test in tests:
            yield (self.atomic,) + test

    def test_add_none(self):
        tests = [
            ('ă', 'a'),
            ('â', 'a'),
            ('ê', 'e'),
            ('ô', 'o'),
            ('ơ', 'o'),
            ('ư', 'u'),
            ('đ', 'd'),

            ('ắấ', 'á'),
            ('ằầ', 'à'),
            ('ẳẩ', 'ả'),
            ('ẵẫ', 'ã'),
            ('ặậ', 'ạ'),

            ('ế', 'é'),
        ]
        for test in tests:
            for subtest in test[0]:
                yield self.atomic, subtest, Mark.NONE, test[1]


class TestAddMark():

    def test_add_mark_at(self):
        eq_(add_mark_at('a', 0, Mark.HAT), 'â')
        eq_(add_mark_at('a', 0, Mark.HORN), 'a')
        eq_(add_mark_at('an', 1, Mark.BREVE), 'an')
        eq_(add_mark_at('đang', 0, Mark.NONE), 'dang')
        eq_(add_mark_at('bẢn', 1, Mark.HAT), 'bẨn')
        eq_(add_mark_at('gang', -1, Mark.HAT), 'gang')
        eq_(add_mark_at('phuô', 3, Mark.HORN), 'phuơ')
        eq_(add_mark_at('uod', 2, Mark.BAR), 'uođ')
        eq_(add_mark_at('D', 0, Mark.BAR), 'Đ')
        eq_(add_mark_at('e', 0, Mark.HAT), 'ê')

    def test_add_mark(self):
        eq_(add_mark(['d', 'uo', 'ng'], Mark.BAR), ['đ', 'uo', 'ng'])
        eq_(add_mark(['d', 'uo', 'ng'], Mark.HORN), ['d', 'ươ', 'ng'])
        eq_(add_mark(['d', 'uô', 'ng'], Mark.HORN), ['d', 'ươ', 'ng'])
        eq_(add_mark(['d', 'Á', ''], Mark.HAT), ['d', 'Ấ', ''])
        eq_(add_mark(['d', '', ''], Mark.BAR), ['đ', '', ''])
        eq_(add_mark(['D', 'uo', 'ng'], Mark.BAR), ['Đ', 'uo', 'ng'])
        eq_(add_mark(['d', 'e', ''], Mark.HAT), ['d', 'ê', ''])
