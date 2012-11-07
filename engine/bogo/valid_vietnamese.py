#!/usr/bin/env python2.7
#-*- coding: utf-8

import utils
import accent
Accent = accent.Accent

CONSONANTS = [
    u'b', u'c', u'd', u'đ', u'',
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

VOWELS= u"àáảãạaằắẳẵặăầấẩẫậâèéẻẽẹeềếểễệêìíỉĩịi" \
        u"òóỏõọoồốổỗộôờớởỡợơùúủũụuừứửữựưỳýỷỹỵy"

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
    u'oi',
    #u'ô',
    u'ơi', #u'oi'
    u'ôi',
    u'ua', u'ui',
    u'ưa', u'ưi', u'ươi', u'ưu', u'uu', u'uoi',
    u'uya',
    u'yêu', u'yeu', 
]

OPEN_COMPOUND_VOWELS = [
    u'oa', u'uye', u'uyê', u'ua',
    u'uâ', u'oo', u'ươ', u'uo', u'uô', u'ưo',
    u'ye', u'yê', u'ie', u'iê',
]


def remove_accent(string):
    for i in range(len(string)):
        if (string[i] in VOWELS) and (not string[i] in u'aăâeêioôơuưy'):
            # Convert á, ả -> a
            # Actually, we're doing 
            # 2, 3 -> 5
            # 6, 8 -> 10
            pos = ((VOWELS.index(string[i]) + 1)/ 6 + 1) * 6 - 1
            string = string[:i] + VOWELS[pos] + string[i+1:]
    return string

def is_valid_combination(components):
    comps = components
    #import pdb; pdb.set_trace()
    # Check if our start sound is a proper consonant
    first_consonant = utils.change_case(comps[0],1)
    if (first_consonant != u'') and (not (first_consonant in CONSONANTS)):
        return False
    
    # And if our ending sound is a proper ending consonant
    if (comps[2] != u'') and (not (comps[2] in ENDING_CONSONANTS)):
        return False
    
    vowel = remove_accent(comps[1])
    if len(vowel) > 1:
        if not (vowel in OPEN_COMPOUND_VOWELS or \
            vowel in CLOSED_COMPOUND_VOWELS):
            return False
    
    if vowel in CLOSED_COMPOUND_VOWELS and comps[2] != u'':
        return False
    
    # 'ăch'?
    if comps[2] == u'ch' and ((vowel in u'ăâeêôơuư') or (vowel in OPEN_COMPOUND_VOWELS)):
        return False
    
    # 'ương' is ok but 'ơng' ?
    if comps[2] == u'ng' and vowel in u'eêơ':
        return False
    
    if comps[2] == u'c' and vowel in u'ê':
        return False
    
    ac = Accent.NONE
    for i in range(len(comps[1])):
        a = accent.get_accent_char(comps[1][i])
        if a != Accent.NONE:
            ac = a
            break
    
    # These consonants can only go with ACUTE, DOT or NONE accents
    if comps[2] in [u'c', u'p', u't', u'ch'] and not ac in [Accent.NONE, Accent.ACUTE, Accent.DOT]:
        return False
    
    return True
