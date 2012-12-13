#!/usr/bin/env python2.7
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
Accent = accent.Accent

CONSONANTS = [
    'b', 'c', 'd', 'đ',
    'g', 'h', 'k', 'l', 'm', 
    'n', 'p', 'q', 'r', 's', 
    't', 'v', 'x', 'ch', 'gh', 
    'kh', 'ph', 'th', 'ng',
    'ngh', 'gi', 'q', 'nh', 'tr'
]

ENDING_CONSONANTS = [
    'c', 'm', 'n', 'p',
    't', 'ch', 'ng', 'nh'
]

# After a closed compound vowel, there can be no consonants whilst there
# can be for an open vowel.
# NOTE: Actually, we'll include their pre-processed form too.
CLOSED_COMPOUND_VOWELS = [
    'ai', 'ao', 'a', 'ay',
    #'ă',
    'â', 'ây', #'a',
    'eo',
    'ê', 'e',
    'ia', 'i', 'iê', 'ie',
    'oa', 'oi', 'oai', 'oay', 'oao', 'oeo',
    #'ô',
    'ơi', #'oi'
    'ôi',
    'ua', 'ui', 'uây', 'uay',
    'ua', 'ưa', 'ưi', 'ươi', 'ư', 'u', 'uoi', 'uôi', 'uê', 'ue', 'ươ', 'uo', 'ưo', 'uy',
    'uy', 'uya', 'uơ',
    'yê', 'ye', 
]

OPEN_COMPOUND_VOWELS = [
    'oa', 'oă', 'oe', 'uye', 'uyê', 'uy', 
    'uâ', 'oo', 'ươ', 'uo', 'uô', 'ưo',
    'ye', 'yê', 'ie', 'iê', 'uê', 'ue', 'uy', 'ua'
]


def is_valid_combination(components):
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
    
    # Allow 'đ' to appear in abbreviations like 'đm', 'đc', 'kgcđ', etc.
    #if comps[0] and not comps[1] and not comps[2] and \
        #not comps[0] in ('gi', 'q'):
        #for c in comps[0]:
            #if not c in CONSONANTS:
                #return False
        #return True
    if comps[0] and not comps[1] and not comps[2]:
        return True
    
    # Check if our start sound is a proper consonant
    if (comps[0] != '') and (not (comps[0] in CONSONANTS)):
        return False
    
    # And if our ending sound is a proper ending consonant
    if (comps[2] != '') and (not (comps[2] in ENDING_CONSONANTS)):
        return False
    
    vowel = accent.remove_accent_string(comps[1])
    if len(vowel) > 1:
        if not (vowel in OPEN_COMPOUND_VOWELS or \
            vowel in CLOSED_COMPOUND_VOWELS):
            return False

    if vowel in CLOSED_COMPOUND_VOWELS and \
        not vowel in OPEN_COMPOUND_VOWELS and comps[2] != '':
        return False
    
    # 'ăch'?
    if comps[2] == 'ch' and ((vowel in 'ăâeôơuư') or \
        (vowel in OPEN_COMPOUND_VOWELS and not vowel in CLOSED_COMPOUND_VOWELS)):
        return False
    
    # 'ương' is ok but 'ơng' ?
    if comps[2] == 'ng' and vowel in ('ơ'):
        return False
    
    # Sadly, this interferes with 'nhếch' :<
    #if comps[2] == 'c' and vowel in 'ê':
    #    return False
    
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
