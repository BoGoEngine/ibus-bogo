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


from . import accent, utils
Accent = accent.Accent

class Mark:
    HAT = 4
    HORN = 3
    BREVE = 2
    BAR = 1
    NONE = 0
    
FAMILY_A = "aăâ"
FAMILY_E = "eê"
FAMILY_O = "oơô"
FAMILY_U = "uư"
FAMILY_D = "dđ"

# TODO: needs refactoring
def add_mark(components, mark):
    comp = list(components)
    if mark == Mark.BAR and comp[0] and comp[0][-1].lower() in FAMILY_D:
        comp[0] = add_mark_at(comp[0], len(comp[0])-1, Mark.BAR)
    else:
        #remove all marks and accents in vowel part
        raw_vowel = accent.add_accent(comp, Accent.NONE)[1].lower()
        raw_vowel = utils.join([add_mark_char(c, Mark.NONE) for c in raw_vowel])
        if mark == Mark.HAT:
            pos = max(raw_vowel.find("a"), raw_vowel.find("o"),
                      raw_vowel.find("e"))
            comp[1] = add_mark_at(comp[1], pos, Mark.HAT)
        elif mark == Mark.BREVE:
            if raw_vowel != "ua":
                comp[1] = add_mark_at(comp[1], raw_vowel.find("a"), Mark.BREVE)
        elif mark == Mark.HORN:
            if raw_vowel in ("uo", "uoi", "uo"):
                comp[1] = utils.join([add_mark_char(c, Mark.HORN) for c in comp[1][:2]]) + comp[1][2:]
            elif raw_vowel == "oa":
                comp[1] = add_mark_at(comp[1], 1, Mark.HORN)
            else:
                pos = max(raw_vowel.find(""), raw_vowel.find("o"))
                comp[1] = add_mark_at(comp[1], pos, Mark.HORN)
    if mark == Mark.NONE:
        if not raw_vowel == comp[1].lower():
            comp[1] = raw_vowel
        elif comp[0] and comp[0][-1] == "đ":
            comp[0][-1] = "d"
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
    if char == "":
        return ""
    case = char.isupper()
    ac = accent.get_accent_char(char)
    char = accent.add_accent_char(char.lower(), Accent.NONE)
    new_char = char
    if mark == Mark.HAT:
        if char in FAMILY_A:
            new_char = "â"
        elif char in FAMILY_O:
            new_char = "ô"
        elif char in FAMILY_E:
            new_char = "ê"
    elif mark == Mark.HORN:
        if char in FAMILY_O:
            new_char = "ơ"
        elif char in FAMILY_U:
            new_char = "ư"
    elif mark == Mark.BREVE:
        if char in FAMILY_A:
            new_char = "ă"
    elif mark == Mark.BAR:
        if char in FAMILY_D:
            new_char = "đ"
    elif mark == Mark.NONE:
        if char in FAMILY_A:
            new_char = "a"
        elif char in FAMILY_E:
            new_char = "e"
        elif char in FAMILY_O:
            new_char = "o"
        elif char in FAMILY_U:
            new_char = "u"
        elif char in FAMILY_D:
            new_char = "d"

    new_char = accent.add_accent_char(new_char, ac)
    return utils.change_case(new_char, case)

def is_valid_mark(comps, mark_trans):
    """
    Check whether the mark given by mark_trans is valid to add to the components
    """
    if mark_trans == "*_":
        return True
    components = list(comps)
    if components[1] != "":
        raw_vowel = accent.add_accent(components, Accent.NONE)[1].lower()
        raw_vowel = utils.join([add_mark_char(c, Mark.NONE) for c in raw_vowel])
    if mark_trans[0] == 'd' and components[0] \
            and components[0][-1].lower() in ("d", "đ"):
        return True
    elif components[1] != "" and raw_vowel.find(mark_trans[0]) != -1:
        return True
    else:
        return False

def remove_mark_char(char):
    """Remove mark from a single character, if any."""
    # TODO: This looks ugly
    if char in FAMILY_A: return "a"
    if char in FAMILY_E: return "e"
    if char in FAMILY_O: return "o"
    if char in FAMILY_U: return "u"
    if char in FAMILY_D: return "d"
    return char

def remove_mark_string(string):
    return utils.join([remove_mark_char(c) for c in string])
