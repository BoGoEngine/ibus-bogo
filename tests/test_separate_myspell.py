#!/usr/bin/env python2.7

import sys
import os.path
import codecs
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'engine')))
    
dictionary = 'vi.dic'

from bogo.new_bogo_engine import *

lines = 0
errors = 0
with codecs.open(dictionary, encoding='utf-8') as f:
    for line in f:
        lines += 1
        if not separate(line.rstrip()):
            print(line.rstrip())
            errors += 1

print("%d fails in %d entries." % (errors, lines))
