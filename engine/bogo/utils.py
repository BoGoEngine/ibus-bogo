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


VOWELS= "àáảãạaằắẳẵặăầấẩẫậâèéẻẽẹeềếểễệêìíỉĩịi" \
        "òóỏõọoồốổỗộôờớởỡợơùúủũụuừứửữựưỳýỷỹỵy"

def join(alist):
    return "".join(alist)

def is_vowel(char):
    char = char.lower()
    return True if (char in VOWELS) else False

def change_case(string, case):
    """
    Helper: Return new string obtained from change the given string to
    desired case.
    
    Args
        string
        case - 0: lower, 1: upper
    """
    return string.upper() if case else string.lower()
    
def append_comps(comps, key):
    c = list(comps)
    if is_vowel(key):
        if not c[2]: pos = 1
        else: pos = 2
    else:
        if not c[2] and not c[1]: pos = 0
        else: pos = 2
    c[pos] += key
    return c
        
