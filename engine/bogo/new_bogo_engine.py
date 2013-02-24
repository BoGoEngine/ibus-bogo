# -*- coding: utf-8 -*-
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
import logging

Mark = mark.Mark
Accent = accent.Accent

# Don't change the following constants or the program will behave
# unexpectedly


class Action:
    ADD_MARK = 2
    ADD_ACCENT = 1
    ADD_CHAR = 0


default_config = {
    "input-method": "telex",
    "output-charset": "utf-8",
    "skip-non-vietnamese": True,
    "available-input-method": {
        'simple-telex': {
            'a': 'a^',
            'o': 'o^',
            'e': 'e^',
            'w': ['u*', 'o*', 'a+'],
            'd': 'd-',
            'f': '\\',
            's': '/',
            'r': '?',
            'x': '~',
            'j': '.',
            # 'z': ['_']
        },
        'telex': {
            'a': 'a^',
            'o': 'o^',
            'e': 'e^',
            'w': ['u*', 'o*', 'a+', '<ư'],
            'd': 'd-',
            'f': '\\',
            's': '/',
            'r': '?',
            'x': '~',
            'j': '.',
            # 'z': ['_'],
            ']': '<ư',
            '[': '<ơ',
            '}': '<Ư',
            '{': '<Ơ'
        },
        'vni': {
            '6': ['a^', 'o^', 'e^'],
            '7': ['u*', 'o*'],
            '8': 'a+',
            '9': 'd-',
            '2': '\\',
            '1': '/',
            '3': '?',
            '4': '~',
            '5': '.',
            # '0': ['_']
        }
    }
}


def is_processable(string):
    return is_valid_combination(separate(string), final_form=False)


def process_key(string, key, raw_string="", config=None):
    logging.debug("== In process_key() ==")
    logging.debug("key = %s", key)

    if config == None:
        config = default_config

    if config["input-method"] in default_config['available-input-method']:
        im = default_config['available-input-method'][config["input-method"]]
    elif 'custom-input-method' in config and \
            config["input-method"] in config['custom-input-method']:
        im = config['custom-input-method'][config["input-method"]]
    else:
        im = default_config['available-input-method'][default_config["input-method"]]

    comps = separate(string)
    logging.debug("separate(string) = %s", str(comps))

    if not is_valid_combination(comps, final_form=False):
        return string + key

    trans_list = get_transformation_list(key, im, raw_string)
    logging.debug("trans_list = %s", str(trans_list))

    new_comps = list(comps)
    for trans in trans_list:
        new_comps = transform(new_comps, trans)

    logging.debug("new_comps: %s", str(new_comps))
    if new_comps == comps:
        # if len(raw_string) >= 2 and raw_string[-1] == raw_string[-2]:
        if can_undo(new_comps, trans_list):
            # The prefix "_" means undo.
            for trans in map(lambda x: "_" + x, trans_list):
                new_comps = transform(new_comps, trans)

        if config["input-method"] == "telex" and \
            len(raw_string) >= 2 and \
            new_comps[1] and new_comps[1][-1].lower() == "u" and \
            raw_string[-2:].lower() == "ww" and \
                not (len(raw_string) >= 3 and raw_string[-3].lower() == "u"):
            new_comps[1] = new_comps[1][:-1]

        # If none of the transformations (if any) work
        # then just append the key
        new_comps = utils.append_comps(new_comps, key)

    return utils.join(new_comps)


def get_transformation_list(key, im, raw_string):
    """
        Return the list of transformations inferred from the entered key. The
        map between transform types and keys is given by module
        bogo_config (if exists) or by variable simple_telex_im

        if entered key is not in im, return "+key", meaning appending
        the entered key to current text
    """
    # if key in im:
    #     lkey = key
    # else:
    #     lkey = key.lower()
    lkey = key.lower()

    if lkey in im:
        if isinstance(im[lkey], list):
            trans_list = im[lkey]
        else:
            trans_list = [im[lkey]]

        for i, trans in enumerate(trans_list):
            if trans[0] == '<' and key.isalpha():
                trans_list[i] = trans[0] + utils.change_case(trans[1], int(key.isupper()))

        if trans_list == ['_']:
            if len(raw_string) >= 2:
                t = list(map(lambda x: "_" + x,
                             get_transformation_list(raw_string[-2], im, raw_string[:-1])))
                # print(t)
                trans_list = t
            else:
                trans_list = ['+' + key]

        return trans_list
    else:
        return ['+' + key]


def get_action(trans):
    """
    Return the action inferred from the transformation `trans`.
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
            return Action.ADD_MARK, Mark.BREVE
        if trans[1] == '*':
            return Action.ADD_MARK, Mark.HORN
        if trans[1] == "-":
            return Action.ADD_MARK, Mark.BAR
        # if trans[1] == "_":
        #     return Action.ADD_MARK, Mark.NONE
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
        # if trans[0] == "_":
        #     return Action.ADD_ACCENT, Accent.NONE


def transform(comps, trans):
    """
    Transform the given string with transform type trans
    """
    logging.debug("== In transform() ==")
    components = list(comps)

    # Special case for 'ư, ơ'
    # if trans[0] == '<' and not trans[1] in ('ư', 'ơ', 'Ư', 'Ơ'):
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
            # Quite a hack. If you want to type giowf = 'giờ', separate()
            # will create ['g', 'i', '']. Therefore we have to allow
            # components[1] == 'i'.
            elif components[1].lower() == 'i' and components[0].lower() == 'g':
                components[1] += trans[1]
                components = separate(utils.join(components))

    if trans[0] == '+':
        # See this and you'll understand:
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

    if trans[0] == '_':
        # Undoing
        return reverse(components, trans[1:])

    action, factor = get_action(trans)
    if action == Action.ADD_ACCENT:
        components = accent.add_accent(components, factor)
    elif action == Action.ADD_MARK:
        if (mark.is_valid_mark(components, trans)):
            components = mark.add_mark(components, factor)
    return components


def separate(string):
    def atomic_separate(string, last_chars, last_is_vowel):
        if string == "" or (last_is_vowel != utils.is_vowel(string[-1])):
            return (string, last_chars)
        else:
            return atomic_separate(string[:-1],
                                   string[-1] + last_chars, last_is_vowel)

    a = atomic_separate(string, "", False)
    b = atomic_separate(a[0], "", True)

    comps = [b[0], b[1], a[1]]

    if a[1] and not b[0] and not b[1]:
        comps.reverse()

    # 'gi' and 'q' need some special treatments
    # We want something like this:
    #     ['g', 'ia', ''] -> ['gi', 'a', '']
    if (comps[0] != '' and comps[1] != '') and \
        ((comps[0] in 'gG' and comps[1][0] in 'iI' and len(comps[1]) > 1) or
         (comps[0] in 'qQ' and comps[1][0] in 'u')):
        comps[0] += comps[1][:1]
        comps[1] = comps[1][1:]

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
    action, factor = get_action(trans)
    comps = list(components)
    string = utils.join(comps)

    if action == Action.ADD_CHAR and string[-1] == trans[1]:
        if comps[2]:
            i = 2
        elif comps[1]:
            i = 1
        else:
            i = 0
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


def can_undo(comps, trans_list):
    comps = list(comps)
    accent_list = list(map(accent.get_accent_char, comps[1]))
    mark_list = list(map(mark.get_mark_char, utils.join(comps)))
    action_list = list(map(lambda x: get_action(x), trans_list))

    a = [action for action in action_list if action[0] == Action.ADD_ACCENT and action[1] in accent_list]
    b = [action for action in action_list if action[0] == Action.ADD_MARK and action[1] in mark_list]
    c = [trans for trans in trans_list if
         trans[0] == "<" and trans[1] in accent.remove_accent_string(comps[1]).lower()]

    if a != [] or b != [] or c != []:
        return True
    else:
        return False
