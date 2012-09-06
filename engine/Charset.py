# -*- encoding: utf-8 -*-
#
# IBus-Bogo - The Vietnamese IME for IBus
#
# Copyright (c) 2012- Long T. Dam <longdt90@gmail.com>,
#                     Trung Ngo <ndtrung4419@gmail.com>
#
# This file is part of IBus-BoGo Project
# IBus-Bogo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# IBus-BoGo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with IBus-BoGo.  If not, see <http://www.gnu.org/licenses/>.
#

tcvn3_charset = ('A','a','¸','¸','µ','µ','¶','¶','·','·','¹','¹',
    '¢','©','Ê','Ê','Ç','Ç','È','È','É','É','Ë','Ë',
    '¡','¨','¾','¾','»','»','¼','¼','½','½','Æ','Æ',
    'B','b','C','c','D','d',
    '§','®',
    'E','e','Ð','Ð','Ì','Ì','Î','Î','Ï','Ï','Ñ','Ñ',
    '£','ª','Õ','Õ','Ò','Ò','Ó','Ó','Ô','Ô','Ö','Ö',
    'F','f','G','g','H','h',
    'I','i','Ý','Ý','×','×','Ø','Ø','Ü','Ü','Þ','Þ',
    'J','j','K','k','L','l','M','m','N','n',
    'O','o','ã','ã','ß','ß','á','á','â','â','ä','ä',
    '¤','«','è','è','å','å','æ','æ','ç','ç','é','é',
    '¥','¬','í','í','ê','ê','ë','ë','ì','ì','î','î',
    'P','p','Q','q','R','r','S','s','T','t',
    'U','u','ó','ó','ï','ï','ñ','ñ','ò','ò','ô','ô',
    '¦','­','ø','ø','õ','õ','ö','ö','÷','÷','ù','ù',
    'V','v','W','w','X','x',
    'Y','y','ý','ý','ú','ú','û','û','ü','ü','þ','þ',
    'Z','z',)

utf8_charset = (u'A',u'a','á',u'á',u'à',u'à',u'ả',u'ả',u'ã',u'ã',u'ạ',u'ạ',
    u'Â',u'â',u'ấ',u'ấ',u'ầ',u'ầ',u'ẩ',u'ẩ',u'ẫ',u'ẫ',u'ậ',u'ậ',
    u'Ă',u'ă',u'ắ',u'ắ',u'ằ',u'ằ',u'ẳ',u'ẳ',u'ẵ',u'ẵ',u'ặ',u'ặ',
    u'B',u'b',u'C',u'c',u'D',u'd',
    u'Đ',u'đ',
    u'E',u'e',u'é',u'é',u'è',u'è',u'ẻ',u'ẻ',u'ẽ',u'ẽ',u'ẹ',u'ẹ',
    u'Ê',u'ê',u'ế',u'ế',u'ề',u'ề',u'ể',u'ể',u'ễ',u'ễ',u'ệ',u'ệ',
    u'F',u'f',u'G',u'g',u'H',u'h',
    u'I',u'i',u'í',u'í',u'ì',u'ì',u'ỉ',u'ỉ',u'ĩ',u'ĩ',u'ị',u'ị',
    u'J',u'j',u'K',u'k',u'L',u'l',u'M',u'm',u'N',u'n',
    u'O',u'o',u'ó',u'ó',u'ò',u'ò',u'ỏ',u'ỏ',u'õ',u'õ',u'ọ',u'ọ',
    u'Ô',u'ô',u'ố',u'ố',u'ồ',u'ồ',u'ổ',u'ổ',u'ỗ',u'ỗ',u'ộ',u'ộ',
    u'Ơ',u'ơ',u'ớ',u'ớ',u'ờ',u'ờ',u'ở',u'ở',u'ỡ',u'ỡ',u'ợ',u'ợ',
    u'P',u'p',u'Q',u'q',u'R',u'r',u'S',u's',u'T',u't',
    u'U',u'u',u'ú',u'ú',u'ù',u'ù',u'ủ',u'ủ',u'ũ',u'ũ',u'ụ',u'ụ',
    u'Ư',u'ư',u'ứ',u'ứ',u'ừ',u'ừ',u'ử',u'ử',u'ữ',u'ữ',u'ự',u'ự',
    u'V',u'v',u'W',u'w',u'X',u'x',
    u'Y',u'y',u'ý',u'ý',u'ỳ',u'ỳ',u'ỷ',u'ỷ',u'ỹ',u'ỹ',u'ỵ',u'ỵ',
    u'Z',u'z',)

def utf8_to_tcvn3(utf8_string):
    tcvn3_string = ""
    for c in utf8_string:
        tcvn3_string += tcvn3_charset[utf8_charset.index(c)]
    return tcvn3_string
