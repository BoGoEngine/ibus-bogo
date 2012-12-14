#!/usr/bin/env python3.2
#-*- coding: utf-8

import sys
import os.path
import codecs
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'engine')))
    
dictionary = os.path.join(os.path.dirname(__file__), 'vi.dic')
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
'palăng',
'tivi',
'tout',
'web'
)

from bogo.new_bogo_engine import *

lines = 0
errors = 0
with open(dictionary) as f:
    for line in f:
        lines += 1
        string = line.rstrip()
        if not separate(string) and not string in known_bad:
            print(string)
            errors += 1

print("%d fails in %d entries." % (errors, lines - len(known_bad) - 1))
