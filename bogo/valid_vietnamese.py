#
# This file is part of ibus-bogo project.
#
# Copyright (C) 2012 Long T. Dam <longdt90@gmail.com>
# Copyright (C) 2012-2013 Trung Ngo <ndtrung4419@gmail.com>
# Copyright (C) 2013 Duong H. Nguyen <cmpitg@gmail.com>
#
# ibus-bogo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ibus-bogo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ibus-bogo.  If not, see <http://www.gnu.org/licenses/>.
#

import collections
from . import accent
from . import mark
from . import utils
Accent = accent.Accent


# Auto-generated list from dictionary
# TODO Think about words composed entirely of vowels
CONSONANTS = set((
    'b', 'c', 'ch', 'd', 'g', 'gh', 'gi', 'h', 'k', 'kh', 'l', 'm', 'n', 'ng',
    'ngh', 'nh', 'p', 'ph', 'qu', 'r', 's', 't', 'th', 'tr', 'v', 'x', 'đ'
))

TERMINAL_CONSONANTS = set((
    'c', 'ch', 'm', 'n', 'ng', 'nh', 'p', 't'
))

NON_TERMINAL_VOWELS = set((
    'a', 'e', 'i', 'iê', 'o', 'oa', 'oe', 'oo', 'oă', 'u', 'uy', 'uyê', 'uâ',
    'uê', 'uô', 'y', 'yê', 'â', 'ê', 'ô', 'ă', 'ơ', 'ư', 'ươ'
))

TERMINAL_VOWELS = set((
    'a', 'ai', 'ao', 'au', 'ay', 'e', 'eo', 'i', 'ia', 'iu', 'iêu', 'o', 'oa',
    'oai', 'oao', 'oay', 'oe', 'oeo', 'oi', 'u', 'ua', 'ui', 'uy', 'uya', 'uyu',
    'uây', 'uê', 'uôi', 'uơ', 'y', 'yêu', 'âu', 'ây', 'ê', 'êu', 'ô', 'ôi', 'ơ',
    'ơi', 'ư', 'ưa', 'ưi', 'ưu', 'ươi', 'ươu'
))


STRIPPED_VOWELS = set([mark.strip(vowel)
                       for vowel in NON_TERMINAL_VOWELS | TERMINAL_VOWELS])

STRIPPED_NON_TERMINAL_VOWELS = set(
    [mark.strip(vowel) for vowel in NON_TERMINAL_VOWELS])

STRIPPED_TERMINAL_VOWELS = set(
    [mark.strip(vowel) for vowel in TERMINAL_VOWELS])


SoundTuple = \
    collections.namedtuple('SoundTuple',
                           'first_consonant vowel last_consonant')


def is_valid_string(string, final_form=True):
    return is_valid_combination(utils.separate(string), final_form)


def is_valid_combination(comp, final_form=True):
    return is_valid_sound_tuple(comp, final_form)


def is_valid_sound_tuple(sound_tuple, final_form=True):
    """Check if a character combination complies to Vietnamese spelling.

    Input:
        sound_tuple - a SoundTuple
        final_form  - whether the tuple represents a complete word
    Output:
        True if the tuple seems to be Vietnamese, False otherwise.
    """

    # We only work with lower case
    sound_tuple = SoundTuple._make(map(str.lower, sound_tuple))

    # Check if our start sound is a proper consonant
    # and if our ending sound is a proper ending consonant
    if (sound_tuple.first_consonant != "" and
            not sound_tuple.first_consonant in CONSONANTS) or \
        (sound_tuple.last_consonant != "" and
            not sound_tuple.last_consonant in TERMINAL_CONSONANTS):
        return False

    # Check our vowel.
    # First remove all accents
    vowel_wo_accent = accent.remove_accent_string(sound_tuple.vowel)

    # We consider words with only a recognized consonant valid.
    # After this test, we can rest asured that vowel_wo_accent is not
    # empty.
    if not vowel_wo_accent:
        return True

    if not final_form:
        # good_vowel = False
        # if comps[2]:
        #     vowel_list = NON_TERMINAL_VOWELS
        #     test = lambda a, b: a == b or mark.remove_mark_string(a) == b
        # else:
        #     vowel_list = TERMINAL_VOWELS + NON_TERMINAL_VOWELS
        #     test = lambda a, b: a == b or a.startswith(b) or mark.remove_mark_string(a).startswith(b)
        # for v in vowel_list:
        #     if test(v, vowel):
        #         good_vowel = True
        #         break
        # if not good_vowel:
        #     return False

        # If the sound_tuple is not complete, we only care whether its vowel
        # position can be transformed into a legit vowel.
        stripped_vowel = mark.strip(vowel_wo_accent)
        return stripped_vowel in STRIPPED_VOWELS

    if not (vowel_wo_accent in NON_TERMINAL_VOWELS | TERMINAL_VOWELS):
        return False

    if sound_tuple.last_consonant != '' and \
            vowel_wo_accent in TERMINAL_VOWELS - NON_TERMINAL_VOWELS:
        return False

    # 'ch' can only go after a, ê, i
    if sound_tuple.last_consonant == 'ch' and \
            (vowel_wo_accent in 'ăâeôơuư' or
                (vowel_wo_accent in NON_TERMINAL_VOWELS - TERMINAL_VOWELS)):
        return False

    # 'ng' can't go after i, ơ
    if sound_tuple.last_consonant == 'ng' and \
            vowel_wo_accent in ('i', 'ơ'):
        return False

    # 'c' can't go after 'i'
    if final_form and sound_tuple.last_consonant == 'c' and \
            vowel_wo_accent == 'i':
        return False

    # Get the first accent
    akzent = Accent.NONE
    for i in range(len(sound_tuple.vowel)):
        a = accent.get_accent_char(sound_tuple.vowel[i])
        if a != Accent.NONE:
            akzent = a
            break

    # These consonants can only go with ACUTE, DOT or NONE accents
    if sound_tuple.last_consonant in ('c', 'p', 't', 'ch') and \
            not akzent in (Accent.NONE, Accent.ACUTE, Accent.DOT):
        return False

    return True
