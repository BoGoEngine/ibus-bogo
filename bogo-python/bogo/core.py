# -*- coding: utf-8 -*-
#
# This file is part of ibus-bogo project.
#
# Copyright (C) 2012 Long T. Dam <longdt90@gmail.com>
# Copyright (C) 2012-2013 Trung Ngo <ndtrung4419@gmail.com>
# Copyright (C) 2013 Duong H. Nguyen <cmpitg@gmail.com>
#
# ibus-bogo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ibus-bogo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ibus-bogo.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Read the docstring for process_sequence() and process_key() first.
"""

from __future__ import unicode_literals
from bogo.validation import is_valid_combination
from bogo import utils, accent, mark
import logging
import sys
import string


Mark = mark.Mark
Accent = accent.Accent


class _Action:
    UNDO = 3
    ADD_MARK = 2
    ADD_ACCENT = 1
    ADD_CHAR = 0


def get_telex_definition(w_shorthand=True, brackets_shorthand=True):
    """Create a definition dictionary for the TELEX input method

    Args:
        w_shorthand (optional): allow a stand-alone w to be
            interpreted as an ư. Default to True.
        brackets_shorthand (optional, True): allow typing ][ as
            shorthand for ươ. Default to True.

    Returns a dictionary to be passed into process_key().
    """
    telex = {
        "a": "a^",
        "o": "o^",
        "e": "e^",
        "w": ["u*", "o*", "a+"],
        "d": "d-",
        "f": "\\",
        "s": "/",
        "r": "?",
        "x": "~",
        "j": ".",
    }

    if w_shorthand:
        telex["w"].append('<ư')

    if brackets_shorthand:
        telex.update({
            "]": "<ư",
            "[": "<ơ",
            "}": "<Ư",
            "{": "<Ơ"
        })

    return telex


def get_vni_definition():
    """Create a definition dictionary for the VNI input method.

    Returns a dictionary to be passed into process_key().
    """
    return {
        "6": ["a^", "o^", "e^"],
        "7": ["u*", "o*"],
        "8": "a+",
        "9": "d-",
        "2": "\\",
        "1": "/",
        "3": "?",
        "4": "~",
        "5": "."
    }


def _accepted_chars(rules):
    if sys.version_info[0] > 2:
        ascii_letters = \
            string.ascii_letters
    else:
        ascii_letters = \
            string.lowercase + \
            string.uppercase

    return set(ascii_letters + ''.join(rules.keys()) + utils.VOWELS + "đ")


def process_sequence(sequence,
                     rules=None,
                     skip_non_vietnamese=True):
    """\
    Convert a key sequence into a Vietnamese string with diacritical marks.

    Args:
        rules (optional): see docstring for process_key().
        skip_non_vietnamese (optional): see docstring for process_key().

    It even supports continous key sequences connected by separators.
    i.e. process_sequence('con meof.ddieen') should work.
    """
    result = ""
    raw = result
    result_parts = []
    if rules is None:
        rules = get_telex_definition()

    accepted_chars = _accepted_chars(rules)

    for key in sequence:
        if key not in accepted_chars:
            result_parts.append(result)
            result_parts.append(key)
            result = ""
            raw = ""
        else:
            result, raw = process_key(
                string=result,
                key=key,
                fallback_sequence=raw,
                rules=rules,
                skip_non_vietnamese=skip_non_vietnamese)

    result_parts.append(result)
    return ''.join(result_parts)


def process_key(string, key,
                fallback_sequence="", rules=None,
                skip_non_vietnamese=True):
    """Process a keystroke.

    Args:
        string: The previously processed string or "".
        key: The keystroke.
        fallback_sequence: The previous keystrokes.
        rules (optional): A dictionary listing
            transformation rules. Defaults to get_telex_definition().
        skip_non_vietnamese (optional): Whether to skip results that
            doesn't seem like Vietnamese. Defaults to True.

    Returns a tuple. The first item of which is the processed
    Vietnamese string, the second item is the next fallback sequence.
    The two items are to be fed back into the next call of process_key()
    as `string` and `fallback_sequence`. If `skip_non_vietnamese` is
    True and the resulting string doesn't look like Vietnamese,
    both items contain the `fallback_sequence`.

    >>> process_key('a', 'a', 'a')
    (â, aa)

    Note that when a key is an undo key, it won't get appended to
    `fallback_sequence`.

    >>> process_key('â', 'a', 'aa')
    (aa, aa)

    `rules` is a dictionary that maps keystrokes to
    their effect string. The effects can be one of the following:

    'a^': a with circumflex (â), only affect an existing 'a family'
    'a+': a with breve (ă), only affect an existing 'a family'
    'e^': e with circumflex (ê), only affect an existing 'e family'
    'o^': o with circumflex (ô), only affect an existing 'o family'
    'o*': o with horn (ơ), only affect an existing 'o family'
    'd-': d with bar (đ), only affect an existing 'd'
    '/': acute (sắc), affect an existing vowel
    '\': grave (huyền), affect an existing vowel
    '?': hook (hỏi), affect an existing vowel
    '~': tilde (ngã), affect an existing vowel
    '.': dot (nặng), affect an existing vowel
    '<ư': append ư
    '<ơ': append ơ

    A keystroke entry can have multiple effects, in which case the
    dictionary entry's value should be a list of the possible
    effect strings. Although you should try to avoid this if
    you are defining a custom input method rule.
    """
    # TODO Figure out a way to remove the `string` argument. Perhaps only the
    #      key sequence is needed?
    def default_return():
        return string + key, fallback_sequence + key

    if rules is None:
        rules = get_telex_definition()

    comps = utils.separate(string)

    # if not _is_processable(comps):
    #     return default_return()

    # Find all possible transformations this keypress can generate
    trans_list = _get_transformation_list(
        key, rules, fallback_sequence)

    # Then apply them one by one
    new_comps = list(comps)
    for trans in trans_list:
        new_comps = _transform(new_comps, trans)

    if new_comps == comps:
        tmp = list(new_comps)

        # If none of the transformations (if any) work
        # then this keystroke is probably an undo key.
        if _can_undo(new_comps, trans_list):
            # The prefix "_" means undo.
            for trans in map(lambda x: "_" + x, trans_list):
                new_comps = _transform(new_comps, trans)

            # Undoing the w key with the TELEX input method with the
            # w:<ư extension requires some care.
            #
            # The input (ư, w) should be undone as w
            # on the other hand, (ư, uw) should return uw.
            #
            # _transform() is not aware of the 2 ways to generate
            # ư in TELEX and always think ư was created by uw.
            # Therefore, after calling _transform() to undo ư,
            # we always get ['', 'u', ''].
            #
            # So we have to clean it up a bit.
            def is_telex_like():
                return '<ư' in rules["w"]

            def undone_vowel_ends_with_u():
                return new_comps[1] and new_comps[1][-1].lower() == "u"

            def not_first_key_press():
                return len(fallback_sequence) >= 1

            def user_typed_ww():
                return (fallback_sequence[-1:]+key).lower() == "ww"

            def user_didnt_type_uww():
                return not (len(fallback_sequence) >= 2 and
                            fallback_sequence[-2].lower() == "u")

            if is_telex_like() and \
                    not_first_key_press() and \
                    undone_vowel_ends_with_u() and \
                    user_typed_ww() and \
                    user_didnt_type_uww():
                # The vowel part of new_comps is supposed to end with
                # u now. That u should be removed.
                new_comps[1] = new_comps[1][:-1]

        if tmp == new_comps:
            fallback_sequence += key
        new_comps = utils.append_comps(new_comps, key)
    else:
        fallback_sequence += key

    if skip_non_vietnamese is True and key.isalpha() and \
            not is_valid_combination(new_comps, final_form=False):
        result = fallback_sequence, fallback_sequence
    else:
        result = utils.join(new_comps), fallback_sequence

    return result


def _get_transformation_list(key, im, fallback_sequence):
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
                trans_list[i] = trans[0] + \
                    utils.change_case(trans[1], int(key.isupper()))

        if trans_list == ['_']:
            if len(fallback_sequence) >= 2:
                # TODO Use takewhile()/dropwhile() to process the last IM keypress
                # instead of assuming it's the last key in fallback_sequence.
                t = list(map(lambda x: "_" + x,
                             _get_transformation_list(fallback_sequence[-2], im,
                                                     fallback_sequence[:-1])))
                # print(t)
                trans_list = t
            # else:
            #     trans_list = ['+' + key]

        return trans_list
    else:
        return ['+' + key]


def _get_action(trans):
    """
    Return the action inferred from the transformation `trans`.
    and the parameter going with this action
    An _Action.ADD_MARK goes with a Mark
    while an _Action.ADD_ACCENT goes with an Accent
    """
    # TODO: VIQR-like convention
    mark_action = {
        '^': (_Action.ADD_MARK, Mark.HAT),
        '+': (_Action.ADD_MARK, Mark.BREVE),
        '*': (_Action.ADD_MARK, Mark.HORN),
        '-': (_Action.ADD_MARK, Mark.BAR),
    }

    accent_action = {
        '\\': (_Action.ADD_ACCENT, Accent.GRAVE),
        '/': (_Action.ADD_ACCENT, Accent.ACUTE),
        '?': (_Action.ADD_ACCENT, Accent.HOOK),
        '~': (_Action.ADD_ACCENT, Accent.TIDLE),
        '.': (_Action.ADD_ACCENT, Accent.DOT),
    }

    if trans[0] in ('<', '+'):
        return _Action.ADD_CHAR, trans[1]
    if trans[0] == "_":
        return _Action.UNDO, trans[1:]
    if len(trans) == 2:
        return mark_action[trans[1]]
    else:
        return accent_action[trans[0]]


def _transform(comps, trans):
    """
    Transform the given string with transform type trans
    """
    logging.debug("== In _transform(%s, %s) ==", comps, trans)
    components = list(comps)

    action, parameter = _get_action(trans)
    if action == _Action.ADD_MARK and \
            components[2] == "" and \
            mark.strip(components[1]).lower() in ['oe', 'oa'] and trans == "o^":
        action, parameter = _Action.ADD_CHAR, trans[0]

    if action == _Action.ADD_ACCENT:
        logging.debug("add_accent(%s, %s)", components, parameter)
        components = accent.add_accent(components, parameter)
    elif action == _Action.ADD_MARK and mark.is_valid_mark(components, trans):
        logging.debug("add_mark(%s, %s)", components, parameter)
        components = mark.add_mark(components, parameter)

        # Handle uơ in "huơ", "thuở", "quở"
        # If the current word has no last consonant and the first consonant
        # is one of "h", "th" and the vowel is "ươ" then change the vowel into
        # "uơ", keeping case and accent. If an alphabet character is then added
        # into the word then change back to "ươ".
        #
        # NOTE: In the dictionary, these are the only words having this strange
        # vowel so we don't need to worry about other cases.
        if accent.remove_accent_string(components[1]).lower() == "ươ" and \
                not components[2] and components[0].lower() in ["", "h", "th", "kh"]:
            # Backup accents
            ac = accent.get_accent_string(components[1])
            components[1] = ("u", "U")[components[1][0].isupper()] + components[1][1]
            components = accent.add_accent(components, ac)

    elif action == _Action.ADD_CHAR:
        if trans[0] == "<":
            if not components[2]:
                # Only allow ư, ơ or ươ sitting alone in the middle part
                # and ['g', 'i', '']. If we want to type giowf = 'giờ', separate()
                # will create ['g', 'i', '']. Therefore we have to allow
                # components[1] == 'i'.
                if (components[0].lower(), components[1].lower()) == ('g', 'i'):
                    components[0] += components[1]
                    components[1] = ''
                if not components[1] or \
                        (components[1].lower(), trans[1].lower()) == ('ư', 'ơ'):
                    components[1] += trans[1]
        else:
            components = utils.append_comps(components, parameter)
            if parameter.isalpha() and \
                    accent.remove_accent_string(components[1]).lower().startswith("uơ"):
                ac = accent.get_accent_string(components[1])
                components[1] = ('ư',  'Ư')[components[1][0].isupper()] + \
                    ('ơ', 'Ơ')[components[1][1].isupper()] + components[1][2:]
                components = accent.add_accent(components, ac)
    elif action == _Action.UNDO:
        components = _reverse(components, trans[1:])

    if action == _Action.ADD_MARK or (action == _Action.ADD_CHAR and parameter.isalpha()):
        # If there is any accent, remove and reapply it
        # because it is likely to be misplaced in previous transformations
        ac = accent.get_accent_string(components[1])

        if ac != accent.Accent.NONE:
            components = accent.add_accent(components, Accent.NONE)
            components = accent.add_accent(components, ac)

    logging.debug("After transform: %s", components)
    return components


def _reverse(components, trans):
    """
    Reverse the effect of transformation 'trans' on 'components'
    If the transformation does not affect the components, return the original
    string.
    """

    action, parameter = _get_action(trans)
    comps = list(components)
    string = utils.join(comps)

    if action == _Action.ADD_CHAR and string[-1].lower() == parameter.lower():
        if comps[2]:
            i = 2
        elif comps[1]:
            i = 1
        else:
            i = 0
        comps[i] = comps[i][:-1]
    elif action == _Action.ADD_ACCENT:
        comps = accent.add_accent(comps, Accent.NONE)
    elif action == _Action.ADD_MARK:
        if parameter == Mark.BAR:
            comps[0] = comps[0][:-1] + \
                mark.add_mark_char(comps[0][-1:], Mark.NONE)
        else:
            if mark.is_valid_mark(comps, trans):
                comps[1] = "".join([mark.add_mark_char(c, Mark.NONE)
                                    for c in comps[1]])
    return comps


def _can_undo(comps, trans_list):
    """
    Return whether a components can be undone with one of the transformation in
    trans_list.
    """
    comps = list(comps)
    accent_list = list(map(accent.get_accent_char, comps[1]))
    mark_list = list(map(mark.get_mark_char, utils.join(comps)))
    action_list = list(map(lambda x: _get_action(x), trans_list))

    def atomic_check(action):
        """
        Check if the `action` created one of the marks, accents, or characters
        in `comps`.
        """
        return (action[0] == _Action.ADD_ACCENT and action[1] in accent_list) \
                or (action[0] == _Action.ADD_MARK and action[1] in mark_list) \
                or (action[0] == _Action.ADD_CHAR and action[1] == \
                    accent.remove_accent_char(comps[1][-1]))  # ơ, ư

    return any(map(atomic_check, action_list))
