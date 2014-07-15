import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from gen_key_sequences import gen_key_sequences

with \
        open("vi-DauCu.dic.filtered") as dictionary, \
        open("../DauCu.sequences", "w")  \
        as output:

    for word in dictionary:
        word = word.rstrip()
        sequences = gen_key_sequences(word)
        for sequence in sequences:
            # output.write(word + " " + sequence + "\n")
            output.write(sequence + ":" + word + "\n")
