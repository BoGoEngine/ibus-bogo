#!/usr/bin/env python2.7
#-*- coding: utf-8

import sys
import os.path
import codecs
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'engine')))
    
dictionary = 'vi.dic'
known_bad = ('ABC',
'ASCII',
'GIF',
'JPEG',
'Telex',
'UBND',
'URL',
'Unicode',
'VIQR',
'VISCII',
'VNI',
'basoi',
'email',
'gram',
'internet',
'intranet',
u'palăng',
'tivi',
'tout',
'web'
)

from bogo.new_bogo_engine import *

lines = 0
errors = 0
with codecs.open(dictionary, encoding='utf-8') as f:
    for line in f:
        lines += 1
        string = line.rstrip()
        if not separate(string) and not string in known_bad:
            print(string)
            errors += 1

print("%d fails in %d entries." % (errors, lines - len(known_bad) - 1))
