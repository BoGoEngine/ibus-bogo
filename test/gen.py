import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "ibus_engine")))

from gen_key_sequences import gen_key_sequences

with open("vi.dic") as dictionary, open("output.sequences", "w") as output:
    for word in dictionary:
        word = word.rstrip()
        sequences = gen_key_sequences(word)
        for sequence in sequences:
        	# output.write(word + " " + sequence + "\n")
        	output.write(sequence + " " + word + "\n")
