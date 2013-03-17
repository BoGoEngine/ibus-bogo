from utils import is_vowel


def _separate(string):
    """
    a -> (-, a, -)
    b -> (b, -, -)

    aa -> (-, aa, -)
    ae -> (-, ae, -)

    bb -> (bb, -, -)
    bc -> (bc, -, -)

    ba -> (b, a, -)
    baa -> (b, aa, -)
    bba -> (bb, a, -)
    bbaa -> (bb, aa, -)

    bac -> (b, a, c)
    bbac -> (bb, a, c)
    baac -> (b, aa, c)
    bacc -> (b, a, cc)

    baca -> (bac, a, -)
    bacaa -> (bac, aa, -)
    bacaacaeb -> (bacaac, ae, b)
    """

    comps = ['', '', '']
    if string == "":
        return comps


def separate(string):
    def atomic_separate(string, last_chars, last_is_vowel):
        if string == "" or (last_is_vowel != is_vowel(string[-1])):
            return (string, last_chars)
        else:
            return atomic_separate(string[:-1],
                string[-1] + last_chars, last_is_vowel)

    a = atomic_separate(string, "", False)
    b = atomic_separate(a[0], "", True)

    if a[1] and not b[0] and not b[1]:
        # Reverse ['', '', 'cc'] -> ['cc', '', '']
        comps = [a[1], '', '']
    else:
        comps = [b[0], b[1], a[1]]


    # 'gi' and 'q' need some special treatments
    # We want something like this:
    #     ['g', 'ia', ''] -> ['gi', 'a', '']
    if (comps[0] != '' and comps[1] != '') and \
    ((comps[0] in 'gG' and comps[1][0] in 'iI' and len(comps[1]) > 1) or \
    (comps[0] in 'qQ' and comps[1][0] in 'u')):
        comps[0] += comps[1][:1]
        comps[1] = comps[1][1:]

    print(comps)

    return comps


if __name__ == '__main__':
    separate("")
    separate("a")
    separate("aoe")
    separate("ac")
    separate("baacc")
    separate("cc")
    separate("c")
    separate("cb")
    separate("gia")
    separate("toán")
    separate("zaaam")
    separate("bacaacaeb")
