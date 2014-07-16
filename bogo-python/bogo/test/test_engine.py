# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from nose.tools import eq_
from nose.plugins.attrib import attr
from functools import partial
import codecs

from bogo.core import _Action, _get_action, process_sequence
from bogo.mark import Mark
import os


process_key_no_skip = partial(process_sequence, skip_non_vietnamese=False)


class TestHelpers():
    def test_transform(self):
        pass

    def test__get_action(self):
        # Add mark
        eq_(_get_action('a^'), (_Action.ADD_MARK, Mark.HAT))
        eq_(_get_action('a+'), (_Action.ADD_MARK, Mark.BREVE))
        eq_(_get_action('o*'), (_Action.ADD_MARK, Mark.HORN))
        eq_(_get_action('d-'), (_Action.ADD_MARK, Mark.BAR))

    def test_get_transformation_list(self):
        pass

    def test_can_undo(self):
        pass

    def test_reverse(self):
        pass


class TestProcessSeq():
    def test_normal_typing(self):
        eq_(process_sequence('v'),     'v')
        eq_(process_sequence('aw'),   'ă')
        eq_(process_sequence('w'),    'ư')
        eq_(process_sequence('ow'),   'ơ')
        eq_(process_sequence('oo'),   'ô')
        eq_(process_sequence('Oo'),   'Ô')
        eq_(process_sequence('dd'),   'đ')
        eq_(process_sequence('muaf'), 'mùa')
        eq_(process_sequence('Doongd'), 'Đông')
        eq_(process_sequence('gif'),  'gì')
        eq_(process_sequence('loAnj'), 'loẠn')
        eq_(process_sequence('muongw'), 'mương')
        eq_(process_sequence('qur'), 'qur')
        eq_(process_sequence('Tosan'), 'Toán')
        eq_(process_sequence('tusnw'), 'tứn')
        eq_(process_sequence('dee'), 'dê')
        eq_(process_sequence('mowis'), 'mới')
        eq_(process_sequence('uwa'), 'ưa')
        eq_(process_sequence('uwo'), 'ưo')
        eq_(process_sequence('ddx'), 'đx')
        eq_(process_sequence('hoacw'), 'hoăc')
        eq_(process_sequence('cuooi'), 'cuôi')

        eq_(process_sequence('tooi'), 'tôi')
        eq_(process_sequence('chuyeenr'), 'chuyển')
        eq_(process_sequence('ddoonjg'), 'động')
        eq_(process_sequence('nheechs'), 'nhếch')

        # uơ related
        eq_(process_sequence('quowr'), 'quở')
        eq_(process_sequence('huow'), 'huơ')
        eq_(process_sequence('thuowr'), 'thuở')
        eq_(process_sequence('QUOWR'), 'QUỞ')
        eq_(process_sequence('HUOW'), 'HUƠ')
        eq_(process_sequence('THUOWR'), 'THUỞ')

        # English words
        eq_(process_key_no_skip('case'), 'cáe')
        eq_(process_key_no_skip('reset'), 'rết')

    @attr('slow')
    def test_with_dictionary(self):
        def atomic(word, sequence):
            eq_(word, process_sequence(sequence))

        path = os.path.join(os.path.dirname(__file__), 'DauCu.sequences')
        with codecs.open(path, "r", "utf-8") as tests:
            for test in tests.read().splitlines():
                sequence, word = test.rstrip().split(":")
                yield atomic, word, sequence

    def test_bugs_related(self):
        # naỳ.
        eq_(process_sequence('nayf.'), 'này.')

        # nguời
        eq_(process_sequence('nguowif'), 'người')
        eq_(process_sequence('nguwowif'), 'người')

        # thươ.
        eq_(process_sequence("thuowr."), "thuở.")

        eq_(process_sequence("[["), "[")
        eq_(process_sequence("[["), "[")

        # BUG #77
        eq_(process_sequence("ddiemer"), "điểm")

        # BUG #78
        eq_(process_sequence("tuoufw"), "tườu")

        # BUG #79
        eq_(process_sequence("huoswc"), "hước")

        # BUG #81
        eq_(process_sequence("khoefo"), "khoèo")

        # BUG #82
        eq_(process_sequence("uorw"), "uở")

    def test_bug_93(self):
        eq_(process_sequence("{{"), "{")
        eq_(process_sequence("}}"), "}")

    def test_free_key_position(self):
        eq_(process_sequence('toios'), 'tối')
        eq_(process_sequence('toois'), 'tối')
        eq_(process_sequence('toosi'), 'tối')

        eq_(process_sequence('tuyenre'), 'tuyển')
        eq_(process_sequence('tuyener'), 'tuyển')
        eq_(process_sequence('tuyeren'), 'tuyển')
        eq_(process_sequence('tuyerne'), 'tuyển')
        eq_(process_sequence('tuyeern'), 'tuyển')
        eq_(process_sequence('tuyeenr'), 'tuyển')

        eq_(process_sequence('tuwrowng'), 'tưởng')

    def test_undo(self):
        eq_(process_sequence('aaa'), 'aa')
        eq_(process_sequence('aww'), 'aw')
        eq_(process_sequence('ass'), 'as')
        eq_(process_sequence('aff'), 'af')
        eq_(process_sequence('arr'), 'ar')
        eq_(process_sequence('axx'), 'ax')
        eq_(process_sequence('ajj'), 'aj')
        eq_(process_sequence('uww'), 'uw')
        eq_(process_sequence('oww'), 'ow')

        eq_(process_sequence('huww'), 'huw')
        eq_(process_sequence('hww'), 'hw')
        eq_(process_sequence('ww'), 'w')
        eq_(process_sequence('uww'), 'uw')

        eq_(process_sequence('DDd'), 'Dd')

        eq_(process_key_no_skip('Loorngr'), 'Lôngr')
        eq_(process_key_no_skip('LOorngr'), 'LÔngr')
        eq_(process_key_no_skip('DDoongd'), 'Dôngd')
        eq_(process_key_no_skip('DDuowngd'), 'Dươngd')
        eq_(process_key_no_skip('Duowngw'), 'Duongw')

    def test_non_vn(self):
        def atomic(word):
            eq_(process_sequence(word), word)

        tests = [
            "system",
            "Virtualbox",
            "VMWare",
            "Microsoft",
            "Google",
            "Installation",
            "teardown",
            "generators",
            "event-driven",
            "flow"
        ]

        for test in tests:
            yield atomic, test

        eq_(process_sequence("aans."), "ấn.")
        eq_(process_sequence("aans]"), "ấn]")
        # eq_(process_sequence("aans.tuongwj"), "ấn.tượng")
        eq_(process_sequence("gi[f"), "giờ")
        # eq_(process_sequence("taojc"), "taojc")

    def test_with_separator(self):
        eq_(process_sequence('con meof dideen'), 'con mèo điên')
        eq_(process_sequence('con.meof'), 'con.mèo')
        eq_(process_sequence('con?meof'), 'con?mèo')

    def test_change_tone(self):
        eq_(process_sequence('meofs'), 'méo')
        eq_(process_sequence('mèos'), 'méo')