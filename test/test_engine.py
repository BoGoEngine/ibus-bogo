from nose.tools import eq_
from functools import partial
from bogo.new_bogo_engine import *
from base_config import BaseConfig
from bogo.mark import Mark
from bogo.accent import Accent

c = BaseConfig("/tmp/ibus-bogo.json")
process_key_dfl = partial(process_key, config=c)

def process_seq(seq, config=c):
    string = ""
    raw = string
    for i in seq:
        raw = raw + i
        string = process_key(string, i, raw_key_sequence=raw,
                             config=config)
    return string


class TestHelpers():
    def test_separate(self):
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
        eq_(separate('QuyÊn'), ['Qu', 'yÊ', 'n'])
        eq_(separate('Trùng'), ['Tr', 'ù', 'ng'])
        eq_(separate('uông'), ['', 'uô', 'ng'])
        eq_(separate('giƯờng'), ['gi', 'Ườ', 'ng'])
        eq_(separate('gi'), ['g', 'i', ''])
        eq_(separate('aoe'), ['', 'aoe', ''])
        eq_(separate('uo'), ['', 'uo', ''])
        eq_(separate('uong'), ['', 'uo', 'ng'])
        eq_(separate('nhếch'), ['nh', 'ế', 'ch'])
        eq_(separate('ếch'), ['', 'ế', 'ch'])
        eq_(separate('xẻng'), ['x', 'ẻ', 'ng'])
        eq_(separate('xoáy'), ['x', 'oáy', ''])
        eq_(separate('quây'), ['qu', 'ây', ''])

    def test_transform(self):
        pass

    def test_get_action(self):
        # Add mark
        eq_(get_action('a^'), (Action.ADD_MARK, Mark.HAT))

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

        # English words
        eq_(process_seq('case'), 'cáe')
        eq_(process_seq('reset'), 'rết')

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