#-*- coding: utf-8
# New BoGo Engine - Vietnamese Text processing engine
#
# Copyright (c) 2012- Long T. Dam <longdt90@gmail.com>,
#                     Trung Ngo <ndtrung4419@gmail.com>
#
# This file is part of BoGo IBus Engine Project BoGo IBus Engine is
# free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# IBus-BoGo is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with IBus-BoGo. If not, see <http://www.gnu.org/licenses/>.

from . import utils
from . import accent
from . import mark
Accent = accent.Accent

# Auto-generated list from dictionary

CONSONANTS = (
'b',
'c',
'ch',
'd',
'g',
'gh',
'gi',
'h',
'k',
'kh',
'l',
'm',
'n',
'ng',
'ngh',
'nh',
'p',
'ph',
'qu',
'r',
's',
't',
'th',
'tr',
'v',
'x',
'đ',
)

ENDING_CONSONANTS = (
'c',
'ch',
'm',
'n',
'ng',
'nh',
'p',
't',
)

OPEN_COMPOUND_VOWELS = (
'a',
'e',
'i',
'iê',
'o',
'oa',
'oe',
'oo',
'oă',
'u',
'uy',
'uyê',
'uâ',
'uê',
'uô',
'y',
'yê',
'â',
'ê',
'ô',
'ă',
'ơ',
'ư',
'ươ',
)

CLOSED_COMPOUND_VOWELS = (
'a',
'ai',
'ao',
'au',
'ay',
'e',
'eo',
'i',
'ia',
'iu',
'iêu',
'o',
'oa',
'oai',
'oao',
'oay',
'oe',
'oeo',
'oi',
'u',
'ua',
'ui',
'uy',
'uya',
'uyu',
'uây',
'uê',
'uôi',
'uơ',
'y',
'yêu',
'âu',
'ây',
'ê',
'êu',
'ô',
'ôi',
'ơ',
'ơi',
'ư',
'ưa',
'ưi',
'ưu',
'ươi',
'ươu',
)

def is_valid_combination(components, final_form = True):
    """Check if a character combination complies to Vietnamese spelling.
    
    Input:
        components - a list of the form ['c', 'a', 'm']
    Output:
        True if OK, False otherwise.
    """
    comps = list(components)
    # We only work with lower case
    for i in range(len(comps)):
        comps[i] = utils.change_case(comps[i], 0)
        
    # Check if our start sound is a proper consonant
    if (comps[0] != '') and (not (comps[0] in CONSONANTS)):
        return False
    
    # And if our ending sound is a proper ending consonant
    if (comps[2] != '') and (not (comps[2] in ENDING_CONSONANTS)):
        return False

    # Check our vowel.
    # First remove all accents
    vowel = accent.remove_accent_string(comps[1])

    # u"chuyển" is the final form whilst "chuyen" is not
    if final_form:
        if len(vowel) > 1:
            if not (vowel in OPEN_COMPOUND_VOWELS or \
                vowel in CLOSED_COMPOUND_VOWELS):
                return False

        if vowel in CLOSED_COMPOUND_VOWELS and \
            not vowel in OPEN_COMPOUND_VOWELS and comps[2] != '':
            return False
    else:
        good_vowel = False
        if comps[2]:
            vowel_list = OPEN_COMPOUND_VOWELS
            test = lambda a, b: a == b or mark.remove_mark_string(a) == b
        else:
            vowel_list = CLOSED_COMPOUND_VOWELS + OPEN_COMPOUND_VOWELS
            test = lambda a, b: a == b or a.startswith(b) or mark.remove_mark_string(a).startswith(b)
        for v in vowel_list:
            if test(v, vowel):
                good_vowel = True
                break
        if not good_vowel:
            return False
    
    # 'ăch'?
    if comps[2] == 'ch' and ((vowel in 'ăâeôơuư') or \
        (vowel in OPEN_COMPOUND_VOWELS and not vowel in CLOSED_COMPOUND_VOWELS)):
        return False
    
    # 'ương' is ok but 'ơng' ?
    if comps[2] == 'ng' and vowel in ('ơ'):
        return False
    
    if final_form and comps[2] == 'c' and vowel in 'ê':
        return False
    
    # Get the first accent
    ac = Accent.NONE
    for i in range(len(comps[1])):
        a = accent.get_accent_char(comps[1][i])
        if a != Accent.NONE:
            ac = a
            break
    
    # These consonants can only go with ACUTE, DOT or NONE accents
    if comps[2] in ['c', 'p', 't', 'ch'] and \
        not ac in [Accent.NONE, Accent.ACUTE, Accent.DOT]:
        return False
    
    return True
