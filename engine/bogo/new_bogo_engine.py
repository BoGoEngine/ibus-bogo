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

from .valid_vietnamese import is_valid_combination
from . import utils, accent, mark

Mark = mark.Mark
Accent = accent.Accent

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
        'w':['u*','o*','a+', '<ư'],
        'd':'d-',
        'f':'\\',
        's':'/',
        'r':'?',
        'x':'~',
        'j':'.',
        'z':'_',
        ']':'<ư',
        '[':'<ơ',
        '}':'<ư',
        '{':'<ơ'
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

class DefaultConfig:
    input_method = 'telex'
    spellchecking = False

def is_processable(string):
    return is_valid_combination(separate(string), final_form = False)

def process_key(string, key, case = 0, config = DefaultConfig()):
    """
    Process the given string and key based on the given input method and
    config.
    
    Args:
        string -
        key -
        case (optional) - Force the output's case. Mostly to determine 
            the case of TELEX's [, ] keys. 0: lower, 1: upper. Default: 0.
        im (optional) - one of 'telex', 'simple-telex', 'vni'.
            Default: 'telex'.
        config - a dictionary.
    """
## SANITY CHECK (scroll down please)
    im = config.input_method
    # People can sometimes be really mischievous :<
    if im in IMs:
        im = IMs[im]
    else:
        im = IMs['telex']

    string = "" if string == None else string

    # Handle non-alpha string like 'tôi_là_ai' by putting 'tôi_là_' in 
    # the `garbage` variable, effectively skipping it then put it back 
    # later.
    # TODO Should this be the ibus engine's job?
    garbage = ''
    for i in range(-1, -len(string)-1, -1): # Reverse indices [-1, -2, -3, ...]
        if not string[i].isalpha():
            garbage += string[:i] + string[i]
            string = '' + string[i+1:] if i != -1 else ''
            break
    
    # Handle process_key('â', '_')
    if not key in im and not key.isalpha():
        string += key
        return garbage + string
    
## END SANITY CHECK (here comes real code)
    
    # Try to break the string down to 3 components
    # separate('chuyen') = ['ch', 'uye', 'n']
    comps = separate(string)
    
    # Refuse to process things like process('zzam', 'f')
    if comps == None:
        return string + key
    
    # Apply transformations
    trans_list = get_transformation_list(key, im, case = case);
    new_comps = comps

    for trans in trans_list:
        new_comps = transform(new_comps, trans)

    # Double typing an IM key to undo.
    # Eg: process_key('à', 'f')
    #  -> transform(['', 'à', ''], '\\') = ['', 'à', '']
    #  -> reverse('à', '\\') = 'a'
    #
    # Note that when undo 'ư' with 'w', this function will always return
    # 'uw' because of lack of raw string information. It is up to the
    # user of this module to change the returned value to 'w' when necessary.
    # 
    if new_comps == comps:
        for trans in trans_list:
            new_comps = reverse(new_comps, trans)
            tmp = list(new_comps)
            if tmp != comps:
                new_comps = utils.append_comps(new_comps, key)
                return garbage + utils.join(new_comps)
        new_comps = utils.append_comps(new_comps, key)
        
    # One last check to rule out cases like 'ảch' or 'chuyểnl'
    if not is_valid_combination(new_comps, final_form = False):
        return string + key
    return garbage + utils.join(new_comps)


def get_transformation_list(key, im, case=0):
    """
        Return list of transformations inferred from entered key.  The
        map between transform types and keys is given by module
        bogo_config (if exists) or by variable simple_telex_im

        if entered key is not in im, return "+key", meaning appending
        the entered key to current text
    """
    if key in im:
        lkey = key
    else:
        lkey = key.lower()

    if lkey in im:
        if isinstance(im[lkey], list):
            trans_list = im[lkey]
        else:
            trans_list = [im[lkey]]
        for i, trans in enumerate(trans_list):
            if trans[0] == '<':
                trans_list[i] = trans[0] + utils.change_case(trans[1], case)
        return trans_list
    else:
        return ['+' + key]


def get_action(trans):
    """
    Return the action inferred from the transformation trans.
    and the factor going with this action
    An Action.ADD_MARK goes with a Mark
    while an Action.ADD_ACCENT goes with an Accent
    """
    if trans[0] in ('<', '+'):
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
    #if trans[0] == '<' and not trans[1] in ('ư', 'ơ', 'Ư', 'Ơ'):
    #        trans = '+' + trans[1]
    # (Not our job)

    if trans[0] == '<':
        if not components[2]:
            # Undo operation
            if components[1][-1:] == trans[1]:
                return components
            # Only allow ư, ơ or ươ sitting alone in the middle part
            elif not components[1] or \
                (components[1].lower() == 'ư' and trans[1].lower() == 'ơ'):
                components[1] += trans[1]
            # Quite a hack. If you want to type gi[f = 'giờ', separate()
            # will create ['g', 'i', '']. Therefore we have to allow
            # components[1] == 'i'.
            elif components[1].lower() == 'i' and components[0].lower() == 'g':
                components[1] += trans[1]
                components = separate(utils.join(components))

    if trans[0] == '+':
        # See this and yo'll understand:
        #   transform(['nn', '', ''],'+n') = ['nnn', '', '']
        #   transform(['c', '', ''],'+o') = ['c', 'o', '']
        #   transform(['c', 'o', ''],'+o') = ['c', 'oo', '']
        #   transform(['c', 'o', ''],'+n') = ['c', 'o', 'n']
        if components[1] == '':
            if utils.is_vowel(trans[1]):
                components[1] += trans[1]
            else:
                components[0] += trans[1]
        else:
            if components[2] == '' and utils.is_vowel(trans[1]):
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
        Otherwise returns [string, '', '']
    """
    comps = ['', '', '']
    if string == '':
        return comps
    
    # Search for the first vowel
    for i in range(len(string)):
        if utils.is_vowel(string[i]):
            comps[0] = '' + string[:i]
            string = '' + string[i:]
            break

    # # No vowel?
    # if comps[0] == '' and not utils.is_vowel(string[0]):
    #     comps[0] = string
    #     string = ''
    
    # Search for the first consonant after the first vowel
    for i in range(len(string)):
        if not utils.is_vowel(string[i]):
            comps[1] = string[:i]
            comps[2] = string[i:]
            break
       
    # No ending consonant? Then the rest of the string must be the vowel part
    if comps[1] == '':
        comps[1] = string
    
    # 'gi' and 'q' need some special treatments
    # We want something like this:
    #     ['g', 'ia', ''] -> ['gi', 'a', '']
    if (comps[0] != '' and comps[1] != '') and \
    ((comps[0] in 'gG' and comps[1][0] in 'iI' and len(comps[1]) > 1) or \
    (comps[0] in 'qQ' and comps[1][0] in 'u')):
        comps[0] += comps[1][:1]
        comps[1] = comps[1][1:]
    
    if not is_valid_combination(comps, final_form = False):
        return [string, '', '']
    
    return comps
    

def reverse(components, trans):
    """
    Reverse the effect of transformation 'trans' on 'components'
    If the transformation does not effect the components, return the original string
    Workflow:
    - Find the part of components that is effected by the transformation
    - Transform this part to the original state (remove accent if the trans
    is ADD_ACCENT action, remove mark if the trans is ADD_MARK action)
    """
    action, factor = get_action (trans)
    comps = list(components)
    string = utils.join(comps)

    if action == Action.ADD_CHAR and string[-1] == trans[1]:
        if comps[2]: i = 2
        elif comps[1] : i = 1
        else: i = 0
        comps[i] = comps[i][:-1]
    elif action == Action.ADD_ACCENT:
        comps = accent.add_accent(comps, Accent.NONE)
    elif action == Action.ADD_MARK:
        if factor == Mark.BAR:
            comps[0] = comps[0][:-1] + \
                mark.add_mark_char(comps[0][-1:], Mark.NONE)
        else:
            if mark.is_valid_mark(comps, trans):
                comps[1] = "".join([mark.add_mark_char(c, Mark.NONE)
                                          for c in comps[1]])
    return comps
