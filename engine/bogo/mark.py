#-*- coding: utf-8

import accent, utils
Accent = accent.Accent

class Mark:
    HAT = 4
    HORN = 3
    BREVE = 2
    BAR = 1
    NONE = 0
    
FAMILY_A = u"aăâ"
FAMILY_E = u"eê"
FAMILY_O = u"oơô"
FAMILY_U = u"uư"
FAMILY_D = u"dđ"

def add_mark(components, mark):
    """
    Case Mark.NONE will be deal with separately by user
    """
    comp = components
    if mark == Mark.BAR and comp[0] and comp[0][-1].lower() in FAMILY_D:
        comp[0] = add_mark_at(comp[0], len(comp[0])-1, Mark.BAR)
    else:
        #remove all marks and accents in vowel part
        raw_vowel = accent.add_accent(comp, Accent.NONE)[1].lower()
        raw_vowel = utils.join([add_mark_char(c, Mark.NONE) for c in raw_vowel])
        if mark == Mark.HAT:
            pos = max(raw_vowel.find(u"a"), raw_vowel.find(u"o"),
                      raw_vowel.find(u"e"))
            comp[1] = add_mark_at(comp[1], pos, Mark.HAT)
        elif mark == Mark.BREVE:
            if raw_vowel != u"ua":
                comp[1] = add_mark_at(comp[1], raw_vowel.find(u"a"), Mark.BREVE)
        elif mark == Mark.HORN:
            if raw_vowel in (u"uo", u"uoi", u"uou"):
                comp[1] = utils.join([add_mark_char(c, Mark.HORN) for c in comp[1][:2]]) + comp[1][2:]
            elif raw_vowel == u"oa":
                comp[1] = add_mark_at(comp[1], 1, Mark.HORN)
            else:
                pos = max(raw_vowel.find(u"u"), raw_vowel.find(u"o"))
                comp[1] = add_mark_at(comp[1], pos, Mark.HORN)
    return comp

def add_mark_at(string, index, mark):
    """
    Add mark to the index-th character of the given string. Return the new string after applying change.
    Notice: index > 0
    """
    if index == -1:
        return string
    # Python can handle the case which index is out of range of given string
    return string[:index] + add_mark_char(string[index], mark) + string[index+1:]

def add_mark_char(char, mark):
    """
    Add mark to a single char.
    """
    if char == u'':
        return u''
    case = char.islower()
    ac = accent.get_accent_char(char)
    char = accent.add_accent_char(char.lower(), Accent.NONE)
    new_char = char
    if mark == Mark.HAT:
        if char in FAMILY_A:
            new_char = u"â"
        elif char in FAMILY_O:
            new_char = u"ô"
        elif char in FAMILY_E:
            new_char = u"ê"
    elif mark == Mark.HORN:
        if char in FAMILY_O:
            new_char = u"ơ"
        elif char in FAMILY_U:
            new_char = u"ư"
    elif mark == Mark.BREVE:
        if char in FAMILY_A:
            new_char = u"ă"
    elif mark == Mark.BAR:
        if char in FAMILY_D:
            new_char = u"đ"
    elif mark == Mark.NONE:
        if char in FAMILY_A:
            new_char = u"a"
        elif char in FAMILY_E:
            new_char = u"e"
        elif char in FAMILY_O:
            new_char = u"o"
        elif char in FAMILY_U:
            new_char = u"u"
        elif char in FAMILY_D:
            new_char = u"d"

    new_char = accent.add_accent_char(new_char, ac)
    return utils.change_case(new_char, case)

def is_valid_mark(comps, mark_trans):
    """
    Check whether the mark given by mark_trans is valid to add to the components
    """
    components = comps
    if components[1] != u"":
        raw_vowel = accent.add_accent(components, Accent.NONE)[1].lower()
        raw_vowel = utils.join([add_mark_char(c, Mark.NONE) for c in raw_vowel])
    if mark_trans[0] == 'd' and components[0] \
            and components[0][-1].lower() in (u"d", u"đ"):
        return True
    elif components[1] != u"" and raw_vowel.find(mark_trans[0]) != -1:
        return True
    else:
        return False
