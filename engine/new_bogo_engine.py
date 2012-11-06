#-*- coding: utf-8
# New BoGo Engine - Vietnamese Text processing engine
#
# Copyright (c) 2012- Long T. Dam <longdt90@gmail.com>,
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

CONFIG_LOADED = False

# Don't change the following constants or the program will behave
# unexpectedly
VOWELS= u"àáảãạaằắẳẵặăầấẩẫậâèéẻẽẹeềếểễệêìíỉĩịi" \
        u"òóỏõọoồốổỗộôờớởỡợơùúủũụuừứửữựưỳýỷỹỵy"

class Accent:
    GRAVE = 5
    ACUTE = 4
    HOOK = 3
    TIDLE= 2
    DOT = 1
    NONE = 0

class Mark:
    HAT = 4
    HORN = 3
    BREVE = 2
    BAR = 1
    NONE = 0

class Action:
    ADD_MARK = 2
    ADD_ACCENT = 1
    ADD_CHAR = 0

FAMILY_A = u"aăâ"
FAMILY_E = u"eê"
FAMILY_O = u"oơô"
FAMILY_U = u"uư"
FAMILY_D = u"dđ"

simple_telex_im = {
    'a':'a^',
    'o':'o^',
    'e':'e^',
    'w':['u*','o*','a+'],
    'd':'d-',
    'f':'\\',
    's':'/',
    'r':'?',
    'x':'~',
    'j':'.',
    'z':'_',
    ']':u'<ư',
    '[':u'<ơ'
    }

def process_key(string, key, im = simple_telex_im):
    trans_list = get_transformation_list(key, im);
    newstring = string
    for trans in trans_list:
        newstring = transform(newstring, trans)

    if newstring == string:
        for trans in trans_list:
            newstring = reverse(newstring, trans)
            if newstring != string:
                break
        newstring += unicode(key)

    if len(newstring) < len(string):
        newstring += unicode(key)
    return newstring;

def get_transformation_list(key, im):
    """
        Return list of transformations inferred from entered key.  The
        map between transform types and keys is given by module
        bogo_config (if exists) or by variable simple_telex_im

        if entered key is not in im, return u"<key", meaning appending
        the entered key to current text
    """

    lkey = key.lower()
    if lkey in im:
        if isinstance(im[lkey], list):
            return im[lkey]
        else:
            return [im[lkey]]
    else:
        return [u'+' + unicode(key)]


def is_vowel(char):
    char = char.lower()
    return True if (char in VOWELS) else False

def separate(string):
    """
    Seperate the given string into 3 parts, based on its structure
    """
    comp = [u'',u'',u'']
    has_vowel = False
    for i in range(len(string)):
        index = -1 - i
        if not string[index].isalpha():
            comp[0] = string[:index] + string[index] + comp[0]
            break
        if not is_vowel(string[index]):
            if not has_vowel:
                comp[2] = string[index] + comp[2]
            else:
                comp[0] = string[:index + 1]
                break
        else:
            has_vowel = True
            comp[1] = string[index] + comp[1]
    # Special consonents qu and gi
    if (comp[0]) and (comp[1]):
        if (comp[0][-1]+comp[1][0]).lower() == u'qu' \
            or ((comp[0][-1]+comp[1][0]).lower() == u'gi' \
                and len(comp[1]) > 1):
            comp[0] += comp[1][0]
            comp[1] = comp[1][1:]
    if not comp[1]:
        comp[0] += comp[2]
        comp[2] = u""
    return comp

def change_case(string, case):
    """
    Helper: Return new string obtained from change the given string to
    desired case case == 0: lower case case == 1: upper case
    """
    return string.lower() if case else string.upper()

def join(alist):
    return u"".join(alist)

def add_accent_char(char, accent):
    """
    Add accent to a single char.  Parameter accent is member of class
    Accent
    """
    if char == u'':
        return u'';
    case = char.islower()
    char = char.lower()
    index = VOWELS.find(char)
    if (index != -1):
        index = index - index % 6 + 5
        char = VOWELS[index - accent]
    return change_case(char, case)

def get_accent_char(char):
    """
    Get accent of an single char
    """
    index = VOWELS.find(char.lower())
    if (index != -1):
        return 5 - index % 6
    else:
        return Accent.NONE

def add_mark_char(char, mark):
    """
    Add mark to a single char.
    """
    if char == u'':
        return u''
    case = char.islower()
    accent = get_accent_char(char)
    char = add_accent_char(char.lower(), Accent.NONE)
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

    new_char = add_accent_char(new_char, accent)
    return change_case(new_char, case)

def add_accent_at(string, mark, accent):
    """
    Add mark to the index-th character of the given string.  Return
    the new string after applying change.
    """
    if index == -1:
        return string
    # Python can handle the case which index is out of range of given string
    return string[:index] + add_accent_char(string[index], accent) \
        + string[index+1:]

def add_accent(components, accent):
    """
    Add accent to the given components.  The parameter components is
    the result of function separate()
    """
    vowel = components[1]
    last_consonant = components[2]
    if accent == Accent.NONE:
        vowel = join([add_accent_char(c, Accent.NONE) for c in vowel])
        return [components[0], vowel, last_consonant]

    if vowel == u"":
        return components
    #raw_string is a list, not a str object
    raw_string = join([add_accent_char(c, Accent.NONE).lower() for c in vowel])
    new_vowel = u""
    # Highest priority for ê and ơ
    index = max(raw_string.find(u"ê"), raw_string.find(u"ơ"))
    if index != -1:
        new_vowel = vowel[:index] + add_accent_char(vowel[index], accent) + vowel[index+1:]
    elif len(vowel) == 1 or (len(vowel) == 2 and last_consonant == u""):
        new_vowel =add_accent_char(vowel[0], accent) + vowel[1:]
    else:
        new_vowel = vowel[:1] + add_accent_char(vowel[1], accent) + vowel[2:]
    return [components[0], new_vowel, components[2]]

def add_mark_at(string, index, mark):
    """
    Add mark to the index-th character of the given string. Return the new string after applying change.
    Notice: index > 0
    """
    if index == -1:
        return string
    # Python can handle the case which index is out of range of given string
    return string[:index] + add_mark_char(string[index], mark) + string[index+1:]

def add_mark(components, mark):
    """
    Case Mark.NONE will be deal with separately by user
    """
    comp = components
    if mark == Mark.BAR and comp[0] and comp[0][-1].lower() in FAMILY_D:
        comp[0] = add_mark_at(comp[0], len(comp[0])-1, Mark.BAR)
    else:
        #remove all marks and accents in vowel part
        raw_vowel = add_accent(comp, Accent.NONE)[1].lower()
        raw_vowel = u"".join([add_mark_char(c, Mark.NONE) for c in raw_vowel])
        if mark == Mark.HAT:
            pos = max(raw_vowel.find(u"a"), raw_vowel.find(u"o"),
                      raw_vowel.find(u"e"))
            comp[1] = add_mark_at(comp[1], pos, Mark.HAT)
        elif mark == Mark.BREVE:
            if raw_vowel != u"ua":
                comp[1] = add_mark_at(comp[1], raw_vowel.find(u"a"), Mark.BREVE)
        elif mark == Mark.HORN:
            if raw_vowel in (u"uo", u"uoi", u"uou"):
                comp[1] = join([add_mark_char(c, Mark.HORN) for c in comp[1][:2]]) + comp[1][2:]
            elif raw_vowel == u"oa":
                comp[1] = add_mark_at(comp[1], 1, Mark.HORN)
            else:
                pos = max(raw_vowel.find(u"u"), raw_vowel.find(u"o"))
                comp[1] = add_mark_at(comp[1], pos, Mark.HORN)
    return comp

def get_action(trans):
    """
    Return the action inferred from the transformation trans.
    and the factor going with this action
    An Action.ADD_MARK goes with a Mark
    while an Action.ADD_ACCENT goes with an Accent
    """
    if trans[0] in (u'<', u'+'):
        return Action.ADD_CHAR, 0
    if len(trans) == 2:
        if trans[1] == '^':
            return Action.ADD_MARK, Mark.HAT
        if trans[1] == '+':
            return Action.ADD_MARK, Mark.BREVE,
        if trans[1] == '*':
            return Action.ADD_MARK, Mark.HORN
        if trans[1] == "-":
            return Action.ADD_MARK, Mark.BAR
    else:
        if trans[0] == "\\":
            return Action.ADD_ACCENT, Accent.GRAVE
        if trans[0] == "/":
            return Action.ADD_ACCENT, Accent.ACUTE
        if trans[0] == "?":
            return Action.ADD_ACCENT, Accent.HOOK
        if trans[0] == "~":
            return Action.ADD_ACCENT, Accent.TIDLE
        if trans[0] == ".":
            return Action.ADD_ACCENT, Accent.DOT
        if trans[0] == "_":
            return Action.ADD_ACCENT, Accent.NONE

def is_valid_mark(components, mark_trans):
    """
    Check whether the mark given by mark_trans is valid to add to the components
    """
    if components[1] != u"":
        raw_vowel = add_accent(components, Accent.NONE)[1].lower()
        raw_vowel = join([add_mark_char(c, Mark.NONE) for c in raw_vowel])
    if mark_trans[0] == 'd' and components[0] \
            and components[0][-1].lower() in (u"d", u"đ"):
        return True
    elif components[1] != u"" and raw_vowel.find(mark_trans[0]) != -1:
        return True
    else:
        return False


def transform(string, trans):
    """
    Transform the given string with transfrom type trans
    """

    if trans[0] == u'<':
        if string[-1:] == trans[1]:
            return string[:-1]
        else:
            string += trans[1]

    if trans[0] == u'+':
        string += trans[1]
        if not trans[1].isalpha():
            return string
        components = separate(string)
        accent = Accent.NONE
        for c in components[1]:
            accent = get_accent_char(c)
            if accent:
                break
        if accent:
            # Remove accent
            components = add_accent(components, Accent.NONE)
            components = add_accent(components, accent)
            return join(components)


    components = separate(string);
    action, factor = get_action (trans)
    if action == Action.ADD_ACCENT:
        components =  add_accent(components, factor)
    elif action == Action.ADD_MARK:
        if (is_valid_mark(components, trans)):
            components = add_mark(components, factor)
    return join(components)

def reverse(string, trans):
    """
    Reverse the effect of transformation trans on string
    If the transformation does not effect the string, return the original string
    Workflow:
    - Find the part of string that is effected by the transformation
    - Transform this part to the original state (remove accent if the trans
    is ADD_ACCENT action, remove mark if the trans is ADD_MARK action)
    """
    action, factor = get_action (trans)
    components = separate(string);

    if action == Action.ADD_ACCENT:
        components = add_accent(components, Accent.NONE)
    elif action == Action.ADD_MARK:
        if factor == Mark.BAR:
            components[0] = components[0][:-1] + \
                add_mark_char(components[0][-1:], Mark.NONE)
        else:
            if is_valid_mark(components, trans):
                components[1] = u"".join([add_mark_char(c, Mark.NONE)
                                          for c in components[1]])
    return join(components)
