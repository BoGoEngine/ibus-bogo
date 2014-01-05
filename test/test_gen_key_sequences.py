from nose.tools import eq_
from .gen_key_sequences import gen_key_sequences

def test_gen_key_sequences():
    eq_(gen_key_sequences("tuyển"),
        set(['tuyeenr', 'tuyeern', 'tuyener', 'tuyenre', 'tuyeren', 'tuyerne']))

    eq_(gen_key_sequences("phan"), set(["phan"]))

    # with open("vi.dic") as dictionary, open("output.sequences", "w") as output:
    #     for word in dictionary:
    #         word = word.rstrip()
    #         output.write(word + " " + str(gen_key_sequences(word)) + "\n")
