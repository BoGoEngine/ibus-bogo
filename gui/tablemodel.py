from PyQt4.QtCore import *
from PyQt4.QtGui import *


UNIKEY_HEADER = 'DO NOT DELETE THIS LINE*** version=1 ***'


def parseUnikeyRules(unikeyFileContent):
    lines = unikeyFileContent.strip().split('\n')
    rules = {}

    if lines[0] == UNIKEY_HEADER:
        for line in lines[1:]:
            abbreviated, expanded = line.split(':')
            rules[abbreviated] = expanded

    return rules


def toUnikeyRules(rules):
    items = sorted(rules.items())
    new_items = "\n".join('%s:%s' % s for s in items)
    return UNIKEY_HEADER + '\n' + new_items + '\n'
