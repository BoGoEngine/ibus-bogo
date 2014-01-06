from bogo import accent, mark
from bogo.utils import separate
from itertools import *


__all__ = ["gen_key_sequences"]


reversed_accents = {
    1: "j",  # DOT
    2: "x",  # TIDLE
    3: "r",  # HOOK
    4: "s",  # ACCUTE
    5: "f"   # GRAVE
}


def unique_everseen(iterable, key=None):
    """
    List unique elements, preserving order. Remember all elements ever seen.

    unique_everseen('AAAABBBCCDAABBB') --> A B C D
    unique_everseen('ABBCcAD', str.lower) --> A B C D
    """
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element


def partition(iterable):
    """
    Separate an iterable into two parts: the blank head and the tail.

    partition(['', '', '', 'r', '']) --> ['', '', ''], ['r', '']
    """
    t1, t2 = tee(iterable)

    def is_blank(value):
        return value == ''
    return takewhile(is_blank, t1), dropwhile(is_blank, t2)


def strip(string):
    """
    Remove all marks and accents from a string.
    """
    return mark.remove_mark_string(accent.remove_accent_string(string))


def make_im_list(word):
    """
    Generate a list of possible input method characters that can be used to
    type the given word. Each IM character is presented as a list of string with
    the IM character in the equivalent position as it would be in the word, all
    other position are empty strings.

    >>> make_im_list("bến")
    [['', 's', ''], ['', 'e', '']]
    """
    im_keys = []

    l = len(word)
    for index, char in enumerate(word):
        ac = accent.get_accent_char(char)
        mk = mark.get_mark_char(char)
        stripped_char = strip(char)

        if ac != accent.Accent.NONE:
            im_keys.append([''] * index + [reversed_accents[ac]] + [''] * (l - index - 1))
        if mk != mark.Mark.NONE:
            if mk in [mark.Mark.HORN, mark.Mark.BREVE]:
                mk = "w"
            else:
                mk = stripped_char
            im_keys.append([''] * index + [mk] + [''] * (l - index - 1))

    return im_keys


def make_permutations(key):
    """
    Create an iterator that generates all possible permutations of an IM character
    from :func:`make_im_list` with the assumption that an IM character can appear
    anywhere after it's base character.

    >>> list(make_permutations(['', 's', '']))
    [['', 's', ''], ['', '', 's']]
    """
    head, tail = partition(key)
    for position in unique_everseen(permutations(tail)):
        head, tmp_head = tee(head)
        yield chain(tmp_head, position)


def recursive_apply(stripped_word, im_list):
    if len(im_list) == 0:
        yield stripped_word
        return

    def apply_im(word, im_map):
        return map("".join, zip(word, im_map))

    for position in make_permutations(im_list[0]):
        new_word = list(apply_im(stripped_word, position))
        if len(im_list) > 1:
            for word in recursive_apply(new_word, im_list[1:]):
                yield word
        else:
            yield new_word


def gen_key_sequences(word):
    """
    Generate possible key sequences that can lead to the given word.

    >>> gen_key_sequences("tuyển")
    set(['tuyeenr', 'tuyeern', 'tuyener', 'tuyenre', 'tuyeren', 'tuyerne'])
    """
    l = len(word)
    stripped_word = strip(word)
    im_keys = make_im_list(word)

    all_im = set()
    for keys in permutations(im_keys):
        for sequence in recursive_apply(stripped_word, keys):
            sequence = "".join(sequence).replace("ww", "w")  # fix consecutive ww
            if "o" in sequence and "u" in sequence and \
                    sequence.count("w") == 2 and sequence.find('o') < sequence.find('w'):  # non-consecutive ones
                last_w = sequence.rfind("w")
                sequence = sequence[:last_w] + sequence[last_w + 1:]
            if strip(separate(word)[1]) == "oo":  # boong, xoong
                sequence = sequence.replace("oo", "ooo")
            all_im.add(sequence)

    return all_im
