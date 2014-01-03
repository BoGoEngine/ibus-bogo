from nose.tools import eq_
from nose.plugins.attrib import attr
from functools import partial

from gi.repository import IBus

from bogo.bogo import *
from base_config import BaseConfig
from bogo.mark import Mark
from bogo.accent import Accent
from .gen_key_sequences import gen_key_sequences
from ibus_engine import Engine

import os

c = BaseConfig("/tmp/ibus-bogo.json")
c_non_vn = BaseConfig("/tmp/ibus-bogo-non-vn.json")
c_non_vn["skip-non-vietnamese"] = True

process_key_dfl = partial(process_key, config=c)
process_key_non_vn = partial(process_key, config=c_non_vn)


def process_seq(seq, config=c):
    string = ""
    raw = string
    for i in seq:
        string, raw = process_key(string,
                                  i,
                                  fallback_sequence=raw,
                                  config=config)
    return string


process_seq_non_vn = partial(process_seq, config=c_non_vn)


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


class TestEngine():
    def test_1_bug_117(self):
        """
        baa + bksp => {new_string: b, raw_string: b}
        """
        eng = Engine()
        eng.do_process_key_event(98, 49, 16) #b
        eng.do_process_key_event(98, 49, IBus.ModifierType.RELEASE_MASK)

        eng.do_process_key_event(97, 30, 16) #a
        eng.do_process_key_event(97, 30, IBus.ModifierType.RELEASE_MASK)

        eng.do_process_key_event(97, 30, 16)
        eng.do_process_key_event(97, 30, IBus.ModifierType.RELEASE_MASK)

        eng.on_backspace_pressed()

        eq_(eng.new_string, 'b')
        eq_(eng._Engine__raw_string, 'b')

    def test_2_bug_117(self):
        """
        bana + bksp => {new_string: bâ, raw_string: baa}
        """
        eng = Engine()
        eng.do_process_key_event(98, 49, 16)
        eng.do_process_key_event(98, 49, IBus.ModifierType.RELEASE_MASK)

        eng.do_process_key_event(97, 30, 16)
        eng.do_process_key_event(97, 30, IBus.ModifierType.RELEASE_MASK)

        eng.do_process_key_event(110, 38, 16) #n
        eng.do_process_key_event(110, 38, IBus.ModifierType.RELEASE_MASK)

        eng.do_process_key_event(97, 30, 16)
        eng.do_process_key_event(97, 30, IBus.ModifierType.RELEASE_MASK)

        eng.on_backspace_pressed()

        eq_(eng.new_string, 'bâ')
        eq_(eng._Engine__raw_string, 'baa')

    def test_3_bug_117(self):
        """
        ba + bksp + a => {new_string: ba, raw_string: ba}
        """
        eng = Engine()
        eng.do_process_key_event(98, 49, 16)
        eng.do_process_key_event(98, 49, IBus.ModifierType.RELEASE_MASK)

        eng.do_process_key_event(97, 30, 16)
        eng.do_process_key_event(97, 30, IBus.ModifierType.RELEASE_MASK)

        eng.on_backspace_pressed()

        eng.do_process_key_event(97, 30, 16)
        eng.do_process_key_event(97, 30, IBus.ModifierType.RELEASE_MASK)

        eq_(eng.new_string, 'ba')
        eq_(eng._Engine__raw_string, 'ba')

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
        eq_(process_seq('Loorngr'), 'Lôngr')
        eq_(process_seq('LOorngr'), 'LÔngr')
        eq_(process_seq('DDoongd'), 'Dôngd')
        eq_(process_seq('DDd'), 'Dd')
        eq_(process_seq('DDuowngd'), 'Dươngd')
        eq_(process_seq('Duowngw'), 'Duongw')
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
        eq_(process_seq('case'), 'cáe')
        eq_(process_seq('reset'), 'rết')

    @attr('slow')
    def test_with_dictionary(self):
        def atomic(word, sequence):
            eq_(word, process_seq(sequence))

        with open(os.path.join(os.path.dirname(__file__), 'vi-DauCu.dic')) as dictionary:
            for word in dictionary.read().splitlines():
                word = word.rstrip()
                for sequence in gen_key_sequences(word):
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
        eq_(process_seq_non_vn("[["), "[")

        # BUG #77
        eq_(process_seq_non_vn("ddiemer"), "điểm")

        # BUG #78
        eq_(process_seq("tuoufw"), "tườu")

        # BUG #79
        eq_(process_seq("huoswc"), "hước")

        # BUG #81
        eq_(process_seq("khoefo"), "khoèo")

        # BUG #82
        eq_(process_seq("uorw"), "uở")

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

    def test_non_vn(self):
        def atomic(word):
            eq_(process_seq(word, config=c_non_vn), word)

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

        eq_(process_seq_non_vn("aans."), "ấn.")
        eq_(process_seq_non_vn("aans]"), "ấn]")
        # eq_(process_seq_non_vn("aans.tuongwj"), "ấn.tượng")
        eq_(process_seq_non_vn("gi[f"), "giờ")
        # eq_(process_seq_non_vn("taojc"), "taojc")
