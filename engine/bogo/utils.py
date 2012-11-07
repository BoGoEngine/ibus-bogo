#-*- coding: utf-8

VOWELS= u"àáảãạaằắẳẵặăầấẩẫậâèéẻẽẹeềếểễệêìíỉĩịi" \
        u"òóỏõọoồốổỗộôờớởỡợơùúủũụuừứửữựưỳýỷỹỵy"

def join(alist):
    return u"".join(alist)

def is_vowel(char):
    char = char.lower()
    return True if (char in VOWELS) else False

def change_case(string, case):
    """
    Helper: Return new string obtained from change the given string to
    desired case case == 0: lower case case == 1: upper case
    """
    return string.lower() if case else string.upper()
