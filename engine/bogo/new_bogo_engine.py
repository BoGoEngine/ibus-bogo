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

from valid_vietnamese import is_valid_combination
import utils, accent, mark

Mark = mark.Mark
Accent = accent.Accent

SKIP_MISSPELLED = True

# Don't change the following constants or the program will behave
# unexpectedly


class Action:
    ADD_MARK = 2
    ADD_ACCENT = 1
    ADD_CHAR = 0

IMs = {
    'simple-telex' : {
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
        'z':'_'
    },
    'telex' : {
        'a':'a^',
        'o':'o^',
        'e':'e^',
        'w':['u*','o*','a+', u'<ư'],
        'W':['u*',u'<Ư'],
        'd':'d-',
        'f':'\\',
        's':'/',
        'r':'?',
        'x':'~',
        'j':'.',
        'z':'_',
        ']':u'<ư',
        '[':u'<ơ'
    },
    'vni' : {
        '6':['a^', 'o^', 'e^'],
        '7':['u*','o*'],
        '8':'a+',
        '9':'d-',
        '2':'\\',
        '1':'/',
        '3':'?',
        '4':'~',
        '5':'.',
        '0':'_'
    }
}

default_config = {
    'skip-misspelled' : True,
    
}

def process_key(string, key, im = 'telex', config = default_config):
    """
    Process the given string and key based on the given input method and
    config.
    """
    ## BEGIN TRICKS (scroll down please)
    
    # People can sometimes be really mischievous :<
    if im in IMs:
        im = IMs[im]
    else:
        im = IMs['telex']

    # Handle non-alpha string like 'tôi_là_ai' by putting 'tôi_là_' in the `garbage` variable,
    # effectively skipping it then put it back later.
    # TODO Should this be the ibus engine's job?
    garbage = u''
    for i in range(-1, -len(string)-1, -1): # Reverse indices [-1, -2, -3, ...]
        if not string[i].isalpha():
            garbage += string[:i] + string[i]
            string = u'' + string[i+1:] if i != -1 else u''
            break
    
    # Handle process_key('â', '_')
    if not key in im and not key.isalpha():
        string += key
        return garbage + string
    
    ## END TRICKS (here comes real code)
    
    # Try to break the string down to 3 components
    # separate('chuyen') = ['ch', 'uye', 'n']
    comps = separate(string)
    # We refuse to process things like process('zzam', 'f')
    if SKIP_MISSPELLED and comps == None:
        return None
    
    # Apply transformations
    trans_list = get_transformation_list(key, im);
    new_comps = comps

    # Special case: enter w 2 times at the beginning of the string =>
    # result is w not uw
    if string in (u'ư', u'Ư') and (key in ('w', 'W')):
        return unicode(key)

    for trans in trans_list:
        new_comps = transform(new_comps, trans)



    # Double typing an IM key to undo.
    # Eg: process_key(u'à', 'f')
    #  -> transform(['', u'à', ''], '\\') = ['', 'à', '']
    #  -> reverse(u'à', '\\') = 'a'
    new_string = utils.join(new_comps)
    if new_string == string:
        for trans in trans_list:
            new_string = reverse(new_string, trans)
            if new_string != string:
                break
        new_string += unicode(key)

    # One last check to rule out cases like 'ảch' or 'chuyểnl'
    if SKIP_MISSPELLED and not is_valid_combination(new_comps):
        return None
    return garbage + new_string;


def get_transformation_list(key, im):
    """
        Return list of transformations inferred from entered key.  The
        map between transform types and keys is given by module
        bogo_config (if exists) or by variable simple_telex_im

        if entered key is not in im, return u"<key", meaning appending
        the entered key to current text
    """
    if key in im:
        lkey = key
    else:
        lkey = key.lower()

    if lkey in im:
        if isinstance(im[lkey], list):
            return im[lkey]
        else:
            return [im[lkey]]
    else:
        return [u'+' + unicode(key)]


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


def transform(comps, trans):
    """
    Transform the given string with transform type trans
    """
    
    components = list(comps)
    
    # Special case for 'ư, ơ'
    if trans[0] == '<' and not trans[1] in (u'ư', u'ơ'):
            trans = '+' + trans[1]

    
            
    
    if trans[0] == u'<':
        if not components[2]:
            # Undo operation
            if components[1][-1:] == trans[1]:
                return components
            # Only allow ư, ơ or ươ sitting alone in the middle part
            elif not components[1] or \
                (components[1] == u'ư' and trans[1] == u'ơ'):
                components[1] += trans[1]
            # Quite a hack. If you want to type gi[f = 'giờ', separate()
            # will create ['g', 'i', '']. Therefore we have to allow
            # components[1] == 'i'.
            elif components[1] == 'i':
                components[1] += trans[1]
                components = separate(utils.join(components))

    if trans[0] == u'+':
        # See this and you'll understand:
        #   transform([u'nn', '', ''],'+n') = [u'nnn', '', '']
        #   transform([u'c', '', ''],'+o') = [u'c', 'o', '']
        #   transform([u'c', 'o', ''],'+o') = [u'c', 'oo', '']
        #   transform([u'c', 'o', ''],'+n') = [u'c', 'o', 'n']
        if components[1] == u'':
            if utils.is_vowel(trans[1]):
                components[1] += trans[1]
            else:
                components[0] += trans[1]
        else:
            if components[2] == u'' and utils.is_vowel(trans[1]):
                components[1] += trans[1]
            else:
                components[2] += trans[1]
        
        # If there is any accent, remove and reapply it
        # because it is likely to be misplaced in previous transformations
        ac = accent.Accent.NONE
        for c in components[1]:
            ac = accent.get_accent_char(c)
            if ac:
                break
        if ac != accent.Accent.NONE:
            # Remove accent
            components = accent.add_accent(components, Accent.NONE)
            components = accent.add_accent(components, ac)
        return components
            
    action, factor = get_action (trans)
    if action == Action.ADD_ACCENT:
        components =  accent.add_accent(components, factor)
    elif action == Action.ADD_MARK:
        if (mark.is_valid_mark(components, trans)):
            components = mark.add_mark(components, factor)
    return components


def separate(string):
    """
        Separates a valid Vietnamese word into 3 components:
        the start sound, the middle sound and the end sound.
        Eg: toán -> [u't', u'oá', u't']
        Otherwise returns None (not a valid Vietnamese word).
    """
    comps = [u'', u'', u'']
    if string == u'':
        return comps
    
    # Search for the first vowel
    for i in range(len(string)):
        if utils.is_vowel(string[i]):
            comps[0] = u'' + string[:i]
            string = u'' + string[i:]
            break

    # No vowel?
    if comps[0] == u'' and not utils.is_vowel(string[0]):
        comps[0] = string
        string = u''
    
    # Search for the first consonant after the first vowel
    for i in range(len(string)):
        if not utils.is_vowel(string[i]):
            comps[1] = string[:i]
            comps[2] = string[i:]
            break
       
    # No ending consonant? Then the rest of the string must be the vowel part
    if comps[1] == u'':
        comps[1] = string
    
    # 'gi' and 'qu' need some special treatments
    # We want something like this:
    #     ['g', 'ia', ''] -> ['gi', 'a', '']
    if (comps[0] != u'' and comps[1] != u'') and \
    ((comps[0] in u'gG' and comps[1][0] in 'iI' and len(comps[1]) > 1) or \
    (comps[0] in u'qQ' and comps[1][0] in 'uU')):
        comps[0] += comps[1][:1]
        comps[1] = comps[1][1:]
    
    if not is_valid_combination(comps) and SKIP_MISSPELLED:
        return None
    return comps
    

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
    components = separate(string)

    if action == Action.ADD_CHAR and string[-1] == trans[1]:
        return string[:-1]
    elif action == Action.ADD_ACCENT:
        components = accent.add_accent(components, Accent.NONE)
    elif action == Action.ADD_MARK:
        if factor == Mark.BAR:
            components[0] = components[0][:-1] + \
                mark.add_mark_char(components[0][-1:], Mark.NONE)
        else:
            if mark.is_valid_mark(components, trans):
                components[1] = u"".join([mark.add_mark_char(c, Mark.NONE)
                                          for c in components[1]])
    return utils.join(components)

