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

import utils
import accent
Accent = accent.Accent

CONSONANTS = [
    u'b', u'c', u'd', u'đ',
    u'g', u'h', u'k', u'l', u'm', 
    u'n', u'p', u'q', u'r', u's', 
    u't', u'v', u'x', u'ch', u'gh', 
    u'kh', u'ph', u'th', u'ng',
    u'ngh', u'gi', u'qu', u'nh', u'tr'
]

ENDING_CONSONANTS = [
    u'c', u'm', u'n', u'p',
    u't', u'ch', u'ng', u'nh'
]

# After a closed compound vowel, there can be no consonants while there
# can be for an open vowel.
# NOTE: Actually, we'll include their pre-processed form too.
CLOSED_COMPOUND_VOWELS = [
    u'ai', u'ao', u'au', u'ay',
    #u'ă',
    u'âu', u'ây', #u'au',
    u'eo',
    u'êu', u'eu',
    u'ia', u'iu', u'iêu',
    u'oi', u'oai',
    #u'ô',
    u'ơi', #u'oi'
    u'ôi',
    u'ua', u'ui',
    u'ưa', u'ưi', u'ươi', u'ưu', u'uu', u'uoi', u'uôi',
    u'uya',
    u'yêu', u'yeu', 
]

OPEN_COMPOUND_VOWELS = [
    u'oa', u'oă', u'oe', u'uye', u'uyê', u'uy', u'ua',
    u'uâ', u'oo', u'ươ', u'uo', u'uô', u'ưo',
    u'ye', u'yê', u'ie', u'iê',
]


def is_valid_combination(components):
    """Check if a character combination complies to Vietnamese spelling.
    
    Input:
        components - a list of the form [u'c', u'a', u'm']
    Output:
        True if OK, False otherwise.
    """
    comps = list(components)
    # We only work with lower case
    for i in range(len(comps)):
        comps[i] = utils.change_case(comps[i], 1)
    
    # Allow 'đ' to appear in abbreviations like 'đm', 'đc', 'kgcđ', etc.
    if comps[0] and not comps[1] and not comps[2] and \
        not comps[0] in ('gi', 'qu'):
        for c in comps[0]:
            if not c in CONSONANTS:
                return False
        return True
    
    # Check if our start sound is a proper consonant
    if (comps[0] != u'') and (not (comps[0] in CONSONANTS)):
        return False
    
    # And if our ending sound is a proper ending consonant
    if (comps[2] != u'') and (not (comps[2] in ENDING_CONSONANTS)):
        return False
    
    vowel = accent.remove_accent_string(comps[1])
    if len(vowel) > 1:
        if not (vowel in OPEN_COMPOUND_VOWELS or \
            vowel in CLOSED_COMPOUND_VOWELS):
            return False

    # Fix oach case. Dirty hack
    if vowel == u'oa' and comps[2] == 'ch':
        return True
        
    # Wrong here: oach?
    if vowel in CLOSED_COMPOUND_VOWELS and comps[2] != u'':
        return False
    
    # 'ăch'?
    if comps[2] == u'ch' and ((vowel in u'ăâeêôơuư') or \
        (vowel in OPEN_COMPOUND_VOWELS)):
        return False
    
    # 'ương' is ok but 'ơng' ?
    if comps[2] == u'ng' and vowel in u'eêơ':
        return False
    
    if comps[2] == u'c' and vowel in u'ê':
        return False
    
    # Get the first accent
    ac = Accent.NONE
    for i in range(len(comps[1])):
        a = accent.get_accent_char(comps[1][i])
        if a != Accent.NONE:
            ac = a
            break
    
    # These consonants can only go with ACUTE, DOT or NONE accents
    if comps[2] in [u'c', u'p', u't', u'ch'] and \
        not ac in [Accent.NONE, Accent.ACUTE, Accent.DOT]:
        return False
    
    return True
