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
CONSONANTS = {
    'b', 'c', 'ch', 'd', 'g', 'gh', 'gi', 'h', 'k', 'kh', 'l', 'm', 'n', 'ng',
    'ngh', 'nh', 'p', 'ph', 'qu', 'r', 's', 't', 'th', 'tr', 'v', 'x', 'đ'
}

TERMINAL_CONSONANTS = {
    'c', 'ch', 'm', 'n', 'ng', 'nh', 'p', 't'
}

VOWELS = {
    'a', 'ai', 'ao', 'au', 'ay', 'e', 'eo', 'i', 'ia', 'iu', 'iê', 'iêu',
    'o', 'oa', 'oai', 'oao', 'oay', 'oe', 'oeo', 'oi', 'oo', 'oă', 'u', 'ua',
    'ui', 'uy', 'uya', 'uyu', 'uyê', 'uâ', 'uây', 'uê', 'uô', 'uôi', 'uơ', 'y',
    'yê', 'yêu', 'â', 'âu', 'ây', 'ê', 'êu', 'ô', 'ôi', 'ă', 'ơ', 'ơi', 'ư',
    'ưa', 'ưi', 'ưu', 'ươ', 'ươi', 'ươu'
}

TERMINAL_VOWELS = {
    'ai', 'ao', 'au', 'ay', 'eo', 'ia', 'iu', 'iêu', 'oai', 'oao', 'oay', 'oeo',
    'oi', 'ua', 'ui', 'uya', 'uyu', 'uây', 'uôi', 'uơ', 'yêu', 'âu', 'ây', 'êu',
    'ôi', 'ơi', 'ưa', 'ưi', 'ưu', 'ươi', 'ươu'
}

STRIPPED_VOWELS = set(map(mark.strip, VOWELS))

STRIPPED_TERMINAL_VOWELS = set(map(mark.strip, TERMINAL_VOWELS))


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

    # Words with no vowel are always valid
    if not sound_tuple.vowel:
        return True

    if final_form:
        result = \
            has_valid_consonants(sound_tuple) and \
            has_valid_vowel(sound_tuple) and \
            has_valid_accent(sound_tuple)
    else:
        result = \
            has_valid_consonants(sound_tuple) and \
            has_valid_vowel_non_final(sound_tuple)

    return result


def has_valid_consonants(sound_tuple):
    # Check if our start sound is a proper consonant
    # and if our ending sound is a proper ending consonant.

    return not (sound_tuple.first_consonant != "" and
                not sound_tuple.first_consonant in CONSONANTS) or \
        (sound_tuple.last_consonant != "" and
         not sound_tuple.last_consonant in TERMINAL_CONSONANTS)


def has_valid_vowel_non_final(sound_tuple):
    # If the sound_tuple is not complete, we only care whether its vowel
    # position can be transformed into a legit vowel.

    stripped_vowel = mark.strip(sound_tuple.vowel)
    if sound_tuple.last_consonant != '':
        return stripped_vowel in STRIPPED_VOWELS - STRIPPED_TERMINAL_VOWELS
    else:
        return stripped_vowel in STRIPPED_VOWELS


def has_valid_vowel(sound_tuple):
    # Check our vowel.
    # First remove all accents
    vowel_wo_accent = accent.remove_accent_string(sound_tuple.vowel)

    if not (vowel_wo_accent in VOWELS):
        return False

    if sound_tuple.last_consonant != '' and \
            vowel_wo_accent in TERMINAL_VOWELS:
        return False

    # 'ch' can only go after a, ê, uê, i, uy, oa
    if sound_tuple.last_consonant == 'ch' and \
            not vowel_wo_accent in {'a', 'ê', 'uê', 'i', 'uy', 'oa'}:
        return False

    # 'c' can't go after 'i' or 'ơ'
    if sound_tuple.last_consonant == 'c' and \
            vowel_wo_accent in {'i', 'ơ'}:
        return False

    # 'ng' can't go after i, ơ
    if sound_tuple.last_consonant == 'ng' and \
            vowel_wo_accent in {'i', 'ơ'}:
        return False

    # 'nh' can only go after a, ê, uy, i, oa, quy
    if sound_tuple.last_consonant == 'nh' and \
            (not vowel_wo_accent in {'a', 'ê', 'i', 'uy', 'oa', 'uê', 'y'} or
            (vowel_wo_accent == 'y' and sound_tuple.first_consonant != 'qu')):
        return False

    return True


def has_valid_accent(sound_tuple):
    # Get the first accent
    akzent = Accent.NONE
    for i in range(len(sound_tuple.vowel)):
        a = accent.get_accent_char(sound_tuple.vowel[i])
        if a != Accent.NONE:
            akzent = a
            break

    # These consonants can only go with ACUTE, DOT accents
    if sound_tuple.last_consonant in {'c', 'p', 't', 'ch'} and \
            not akzent in {Accent.ACUTE, Accent.DOT}:
        return False

    return True
