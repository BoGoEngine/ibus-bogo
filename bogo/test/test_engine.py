from nose.tools import eq_
from nose.plugins.attrib import attr
from functools import partial

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
        eq_(process_seq('v'), 'v')
        eq_(process_seq('aw'), 'ă')
        eq_(process_seq('w'), 'ư')
        eq_(process_seq('ow'), 'ơ')
        eq_(process_seq('oo'), 'ô')
        eq_(process_seq('Oo'), 'Ô')
        eq_(process_seq('dd'), 'đ')
        eq_(process_seq('muaf'), 'mùa')
        eq_(process_seq('Doongd'), 'Đông')
        eq_(process_seq('gif'), 'gì')
        eq_(process_seq('loAnj'), 'loẠn')
        eq_(process_seq('muongw'), 'mương')
        eq_(process_seq('qur'), 'qur')
        eq_(process_seq('Tosan'), 'Toán')
        eq_(process_seq('tusnw'), 'tứn')
        eq_(process_seq('dee'), 'dê')
        eq_(process_seq('mowis'), 'mới')
        eq_(process_seq('uwa'), 'ưa')
        eq_(process_seq('uwo'), 'ưo')
        eq_(process_seq('ddx'), 'đx')
        eq_(process_seq('hoacw'), 'hoăc')
        eq_(process_seq('cuooi'), 'cuôi')

        eq_(process_seq('tooi'), 'tôi')
        eq_(process_seq('chuyeenr'), 'chuyển')
        eq_(process_seq('ddoonjg'), 'động')
        eq_(process_seq('nheechs'), 'nhếch')

        # uơ related
        eq_(process_seq('quowr'), 'quở')
        eq_(process_seq('huow'), 'huơ')
        eq_(process_seq('thuowr'), 'thuở')
        eq_(process_seq('QUOWR'), 'QUỞ')
        eq_(process_seq('HUOW'), 'HUƠ')
        eq_(process_seq('THUOWR'), 'THUỞ')

        # English words
        eq_(process_key_no_skip('case'), 'cáe')
        eq_(process_key_no_skip('reset'), 'rết')

    @attr('slow')
    def test_with_dictionary(self):
        def atomic(word, sequence):
            eq_(word, process_seq(sequence))

        path = os.path.join(os.path.dirname(__file__), 'DauCu.sequences')
        with open(path) as tests:
            for test in tests.read().splitlines():
                sequence, word = test.rstrip().split(":")
                yield atomic, word, sequence

    def test_bugs_related(self):
        # naỳ.
        eq_(process_seq('nayf.'), 'này.')

        # nguời
        eq_(process_seq('nguowif'), 'người')
        eq_(process_seq('nguwowif'), 'người')

        # thươ.
        eq_(process_seq("thuowr."), "thuở.")

        eq_(process_seq("[["), "[")
        eq_(process_seq("[["), "[")

        # BUG #77
        eq_(process_seq("ddiemer"), "điểm")

        # BUG #78
        eq_(process_seq("tuoufw"), "tườu")

        # BUG #79
        eq_(process_seq("huoswc"), "hước")

        # BUG #81
        eq_(process_seq("khoefo"), "khoèo")

        # BUG #82
        eq_(process_seq("uorw"), "uở")

    def test_bug_93(self):
        eq_(process_seq("{{"), "{")
        eq_(process_seq("}}"), "}")

    def test_free_key_position(self):
        eq_(process_seq('toios'), 'tối')
        eq_(process_seq('toois'), 'tối')
        eq_(process_seq('toosi'), 'tối')

        eq_(process_seq('tuyenre'), 'tuyển')
        eq_(process_seq('tuyener'), 'tuyển')
        eq_(process_seq('tuyeren'), 'tuyển')
        eq_(process_seq('tuyerne'), 'tuyển')
        eq_(process_seq('tuyeern'), 'tuyển')
        eq_(process_seq('tuyeenr'), 'tuyển')

        eq_(process_seq('tuwrowng'), 'tưởng')

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

        eq_(process_key_no_skip('Loorngr'), 'Lôngr')
        eq_(process_key_no_skip('LOorngr'), 'LÔngr')
        eq_(process_key_no_skip('DDoongd'), 'Dôngd')
        eq_(process_key_no_skip('DDuowngd'), 'Dươngd')
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

        eq_(process_seq("aans."), "ấn.")
        eq_(process_seq("aans]"), "ấn]")
        # eq_(process_seq("aans.tuongwj"), "ấn.tượng")
        eq_(process_seq("gi[f"), "giờ")
        # eq_(process_seq("taojc"), "taojc")
