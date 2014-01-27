# -*- coding: utf-8 -*-

from nose.tools import eq_
from nose.plugins.attrib import attr
from functools import partial
import codecs

from bogo.bogo import *
from bogo.mark import Mark
import os

test_config = {
    "input-method": "telex",
    "skip-non-vietnamese": True
}

test_config_no_skip = {
    "input-method": "telex",
    "skip-non-vietnamese": False
}


def process_seq(seq, config=test_config):
    string = ""
    raw = string
    for i in seq:
        string, raw = process_key(string,
                                  i,
                                  fallback_sequence=raw,
                                  config=config)
    return string


process_key_no_skip = partial(process_seq, config=test_config_no_skip)


class TestHelpers():
    def test_transform(self):
        pass

    def test_get_action(self):
        # Add mark
        eq_(get_action('a^'), (Action.ADD_MARK, Mark.HAT))
        eq_(get_action('a+'), (Action.ADD_MARK, Mark.BREVE))
        eq_(get_action('o*'), (Action.ADD_MARK, Mark.HORN))
        eq_(get_action('d-'), (Action.ADD_MARK, Mark.BAR))

    def test_get_transformation_list(self):
        pass

    def test_can_undo(self):
        pass

    def test_reverse(self):
        pass


class TestProcessSeq():
    def test_normal_typing(self):
        eq_(process_seq('v'),     'v')
        eq_(process_seq('aw'),   u'ă')
        eq_(process_seq('w'),    u'ư')
        eq_(process_seq('ow'),   u'ơ')
        eq_(process_seq('oo'),   u'ô')
        eq_(process_seq('Oo'),   u'Ô')
        eq_(process_seq('dd'),   u'đ')
        eq_(process_seq('muaf'), u'mùa')
        eq_(process_seq('Doongd'), u'Đông')
        eq_(process_seq('gif'),  u'gì')
        eq_(process_seq('loAnj'), u'loẠn')
        eq_(process_seq('muongw'), u'mương')
        eq_(process_seq('qur'), 'qur')
        eq_(process_seq('Tosan'), u'Toán')
        eq_(process_seq('tusnw'), u'tứn')
        eq_(process_seq('dee'), u'dê')
        eq_(process_seq('mowis'), u'mới')
        eq_(process_seq('uwa'), u'ưa')
        eq_(process_seq('uwo'), u'ưo')
        eq_(process_seq('ddx'), u'đx')
        eq_(process_seq('hoacw'), u'hoăc')
        eq_(process_seq('cuooi'), u'cuôi')

        eq_(process_seq('tooi'), u'tôi')
        eq_(process_seq('chuyeenr'), u'chuyển')
        eq_(process_seq('ddoonjg'), u'động')
        eq_(process_seq('nheechs'), u'nhếch')

        # uơ related
        eq_(process_seq('quowr'), u'quở')
        eq_(process_seq('huow'), u'huơ')
        eq_(process_seq('thuowr'), u'thuở')
        eq_(process_seq('QUOWR'), u'QUỞ')
        eq_(process_seq('HUOW'), u'HUƠ')
        eq_(process_seq('THUOWR'), u'THUỞ')

        # English words
        eq_(process_key_no_skip('case'), u'cáe')
        eq_(process_key_no_skip('reset'), u'rết')

    @attr('slow')
    def test_with_dictionary(self):
        def atomic(word, sequence):
            eq_(word, process_seq(sequence))

        path = os.path.join(os.path.dirname(__file__), 'DauCu.sequences')
        with codecs.open(path, "r", "utf-8") as tests:
            for test in tests.read().splitlines():
                sequence, word = test.rstrip().split(":")
                yield atomic, word, sequence

    def test_bugs_related(self):
        # naỳ.
        eq_(process_seq('nayf.'), u'này.')

        # nguời
        eq_(process_seq('nguowif'), u'người')
        eq_(process_seq('nguwowif'), u'người')

        # thươ.
        eq_(process_seq("thuowr."), u"thuở.")

        eq_(process_seq("[["), "[")
        eq_(process_seq("[["), "[")

        # BUG #77
        eq_(process_seq("ddiemer"), u"điểm")

        # BUG #78
        eq_(process_seq("tuoufw"), u"tườu")

        # BUG #79
        eq_(process_seq("huoswc"), u"hước")

        # BUG #81
        eq_(process_seq("khoefo"), u"khoèo")

        # BUG #82
        eq_(process_seq("uorw"), u"uở")

    def test_bug_93(self):
        eq_(process_seq("{{"), "{")
        eq_(process_seq("}}"), "}")

    def test_free_key_position(self):
        eq_(process_seq('toios'), u'tối')
        eq_(process_seq('toois'), u'tối')
        eq_(process_seq('toosi'), u'tối')

        eq_(process_seq('tuyenre'), u'tuyển')
        eq_(process_seq('tuyener'), u'tuyển')
        eq_(process_seq('tuyeren'), u'tuyển')
        eq_(process_seq('tuyerne'), u'tuyển')
        eq_(process_seq('tuyeern'), u'tuyển')
        eq_(process_seq('tuyeenr'), u'tuyển')

        eq_(process_seq('tuwrowng'), u'tưởng')

    def test_undo(self):
        eq_(process_seq('aaa'), 'aa')
        eq_(process_seq('aww'), 'aw')
        eq_(process_seq('ass'), 'as')
        eq_(process_seq('aff'), 'af')
        eq_(process_seq('arr'), 'ar')
        eq_(process_seq('axx'), 'ax')
        eq_(process_seq('ajj'), 'aj')
        eq_(process_seq('uww'), 'uw')
        eq_(process_seq('oww'), 'ow')

        eq_(process_seq('huww'), 'huw')
        eq_(process_seq('hww'), 'hw')
        eq_(process_seq('ww'), 'w')
        eq_(process_seq('uww'), 'uw')

        eq_(process_seq('DDd'), 'Dd')

        eq_(process_key_no_skip('Loorngr'), u'Lôngr')
        eq_(process_key_no_skip('LOorngr'), u'LÔngr')
        eq_(process_key_no_skip('DDoongd'), u'Dôngd')
        eq_(process_key_no_skip('DDuowngd'), u'Dươngd')
        eq_(process_key_no_skip('Duowngw'), 'Duongw')

    def test_non_vn(self):
        def atomic(word):
            eq_(process_seq(word), word)

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

        eq_(process_seq("aans."), u"ấn.")
        eq_(process_seq("aans]"), u"ấn]")
        # eq_(process_seq("aans.tuongwj"), "ấn.tượng")
        eq_(process_seq("gi[f"), u"giờ")
        # eq_(process_seq("taojc"), "taojc")
