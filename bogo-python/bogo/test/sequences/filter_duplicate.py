"""
Filter out syllables with duplicated vowel and last consonant.
For example: only one of khương and thương needs to be tested.
"""


from collections import defaultdict
import bogo

families = defaultdict(list)

with open("vi-DauCu.dic") as f:
    syllables = f.read().split()

for syllable in syllables:
    head, vowel, tail = bogo.utils.separate(syllable)
    families[bogo.accent.remove_accent_string(vowel + tail)].append(syllable)

for syllable_group in families.values():
    needed_tones = [0, 1, 2, 3, 4, 5]
    for syllable in syllable_group:
        tone = bogo.accent.get_accent_string(syllable)
        if tone in needed_tones:
            print(syllable)
            needed_tones.remove(tone)
            if needed_tones == []:
                break
