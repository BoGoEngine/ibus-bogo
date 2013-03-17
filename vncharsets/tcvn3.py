""" Python Character Mapping Codec tcvn3 generated from 'charset-data/TCVN3.txt' with gencodec.py.

"""#"

import codecs

### Codec APIs

class Codec(codecs.Codec):

    def encode(self,input,errors='strict'):
        return codecs.charmap_encode(input,errors,encoding_table)

    def decode(self,input,errors='strict'):
        return codecs.charmap_decode(input,errors,decoding_table)

class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final=False):
        return codecs.charmap_encode(input,self.errors,encoding_table)[0]

class IncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input, final=False):
        return codecs.charmap_decode(input,self.errors,decoding_table)[0]

class StreamWriter(Codec,codecs.StreamWriter):
    pass

class StreamReader(Codec,codecs.StreamReader):
    pass

### encodings module API

def getregentry():
    return codecs.CodecInfo(
        name='tcvn3',
        encode=Codec().encode,
        decode=Codec().decode,
        incrementalencoder=IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
        streamreader=StreamReader,
        streamwriter=StreamWriter,
    )


### Decoding Table

decoding_table = (
    '\x00'      #  0x00 -> CONTROL CHARACTER
    '\x01'      #  0x01 -> CONTROL CHARACTER
    '\x02'      #  0x02 -> CONTROL CHARACTER
    '\x03'      #  0x03 -> CONTROL CHARACTER
    '\x04'      #  0x04 -> CONTROL CHARACTER
    '\x05'      #  0x05 -> CONTROL CHARACTER
    '\x06'      #  0x06 -> CONTROL CHARACTER
    '\x07'      #  0x07 -> CONTROL CHARACTER
    '\x08'      #  0x08 -> CONTROL CHARACTER
    '\t'        #  0x09 -> CONTROL CHARACTER
    '\n'        #  0x0A -> CONTROL CHARACTER
    '\x0b'      #  0x0B -> CONTROL CHARACTER
    '\x0c'      #  0x0C -> CONTROL CHARACTER
    '\r'        #  0x0D -> CONTROL CHARACTER
    '\x0e'      #  0x0E -> CONTROL CHARACTER
    '\x0f'      #  0x0F -> CONTROL CHARACTER
    '\x10'      #  0x10 -> CONTROL CHARACTER
    '\x11'      #  0x11 -> CONTROL CHARACTER
    '\x12'      #  0x12 -> CONTROL CHARACTER
    '\x13'      #  0x13 -> CONTROL CHARACTER
    '\x14'      #  0x14 -> CONTROL CHARACTER
    '\x15'      #  0x15 -> CONTROL CHARACTER
    '\x16'      #  0x16 -> CONTROL CHARACTER
    '\x17'      #  0x17 -> CONTROL CHARACTER
    '\x18'      #  0x18 -> CONTROL CHARACTER
    '\x19'      #  0x19 -> CONTROL CHARACTER
    '\x1a'      #  0x1A -> CONTROL CHARACTER
    '\x1b'      #  0x1B -> CONTROL CHARACTER
    '\x1c'      #  0x1C -> CONTROL CHARACTER
    '\x1d'      #  0x1D -> CONTROL CHARACTER
    '\x1e'      #  0x1E -> CONTROL CHARACTER
    '\x1f'      #  0x1F -> CONTROL CHARACTER
    ' '         #  0x20 -> 0x20
    '!'         #  0x21 -> 0x21
    '"'         #  0x22 -> 0x22
    '#'         #  0x23 -> 0x23
    '$'         #  0x24 -> 0x24
    '%'         #  0x25 -> 0x25
    '&'         #  0x26 -> 0x26
    "'"         #  0x27 -> 0x27
    '('         #  0x28 -> 0x28
    ')'         #  0x29 -> 0x29
    '*'         #  0x2A -> 0x2a
    '+'         #  0x2B -> 0x2b
    ','         #  0x2C -> 0x2c
    '-'         #  0x2D -> 0x2d
    '.'         #  0x2E -> 0x2e
    '/'         #  0x2F -> 0x2f
    '0'         #  0x30 -> 0x30
    '1'         #  0x31 -> 0x31
    '2'         #  0x32 -> 0x32
    '3'         #  0x33 -> 0x33
    '4'         #  0x34 -> 0x34
    '5'         #  0x35 -> 0x35
    '6'         #  0x36 -> 0x36
    '7'         #  0x37 -> 0x37
    '8'         #  0x38 -> 0x38
    '9'         #  0x39 -> 0x39
    ':'         #  0x3A -> 0x3a
    ';'         #  0x3B -> 0x3b
    '<'         #  0x3C -> 0x3c
    '='         #  0x3D -> 0x3d
    '>'         #  0x3E -> 0x3e
    '?'         #  0x3F -> 0x3f
    '@'         #  0x40 -> 0x40
    'A'         #  0x41 -> 0x41
    'B'         #  0x42 -> 0x42
    'C'         #  0x43 -> 0x43
    'D'         #  0x44 -> 0x44
    'E'         #  0x45 -> 0x45
    'F'         #  0x46 -> 0x46
    'G'         #  0x47 -> 0x47
    'H'         #  0x48 -> 0x48
    'I'         #  0x49 -> 0x49
    'J'         #  0x4A -> 0x4a
    'K'         #  0x4B -> 0x4b
    'L'         #  0x4C -> 0x4c
    'M'         #  0x4D -> 0x4d
    'N'         #  0x4E -> 0x4e
    'O'         #  0x4F -> 0x4f
    'P'         #  0x50 -> 0x50
    'Q'         #  0x51 -> 0x51
    'R'         #  0x52 -> 0x52
    'S'         #  0x53 -> 0x53
    'T'         #  0x54 -> 0x54
    'U'         #  0x55 -> 0x55
    'V'         #  0x56 -> 0x56
    'W'         #  0x57 -> 0x57
    'X'         #  0x58 -> 0x58
    'Y'         #  0x59 -> 0x59
    'Z'         #  0x5A -> 0x5a
    '['         #  0x5B -> 0x5b
    '\\'        #  0x5C -> 0x5c
    ']'         #  0x5D -> 0x5d
    '^'         #  0x5E -> 0x5e
    '_'         #  0x5F -> 0x5f
    '`'         #  0x60 -> 0x60
    'a'         #  0x61 -> 0x61
    'b'         #  0x62 -> 0x62
    'c'         #  0x63 -> 0x63
    'd'         #  0x64 -> 0x64
    'e'         #  0x65 -> 0x65
    'f'         #  0x66 -> 0x66
    'g'         #  0x67 -> 0x67
    'h'         #  0x68 -> 0x68
    'i'         #  0x69 -> 0x69
    'j'         #  0x6A -> 0x6a
    'k'         #  0x6B -> 0x6b
    'l'         #  0x6C -> 0x6c
    'm'         #  0x6D -> 0x6d
    'n'         #  0x6E -> 0x6e
    'o'         #  0x6F -> 0x6f
    'p'         #  0x70 -> 0x70
    'q'         #  0x71 -> 0x71
    'r'         #  0x72 -> 0x72
    's'         #  0x73 -> 0x73
    't'         #  0x74 -> 0x74
    'u'         #  0x75 -> 0x75
    'v'         #  0x76 -> 0x76
    'w'         #  0x77 -> 0x77
    'x'         #  0x78 -> 0x78
    'y'         #  0x79 -> 0x79
    'z'         #  0x7A -> 0x7a
    '{'         #  0x7B -> 0x7b
    '|'         #  0x7C -> 0x7c
    '}'         #  0x7D -> 0x7d
    '~'         #  0x7E -> 0x7e
    '\x7f'      #  0x7F -> CONTROL CHARACTER
    '\x80'      #  0x80 -> 0x80
    '\x81'      #  0x81 -> 0x81
    '\x82'      #  0x82 -> 0x82
    '\x83'      #  0x83 -> 0x83
    '\x84'      #  0x84 -> 0x84
    '\x85'      #  0x85 -> 0x85
    '\x86'      #  0x86 -> 0x86
    '\x87'      #  0x87 -> 0x87
    '\x88'      #  0x88 -> 0x88
    '\x89'      #  0x89 -> 0x89
    '\x8a'      #  0x8A -> 0x8a
    '\x8b'      #  0x8B -> 0x8b
    '\x8c'      #  0x8C -> 0x8c
    '\x8d'      #  0x8D -> 0x8d
    '\x8e'      #  0x8E -> 0x8e
    '\x8f'      #  0x8F -> 0x8f
    '\x90'      #  0x90 -> 0x90
    '\x91'      #  0x91 -> 0x91
    '\x92'      #  0x92 -> 0x92
    '\x93'      #  0x93 -> 0x93
    '\x94'      #  0x94 -> 0x94
    '\x95'      #  0x95 -> 0x95
    '\x96'      #  0x96 -> 0x96
    '\x97'      #  0x97 -> 0x97
    '\x98'      #  0x98 -> 0x98
    '\x99'      #  0x99 -> 0x99
    '\x9a'      #  0x9A -> 0x9a
    '\x9b'      #  0x9B -> 0x9b
    '\x9c'      #  0x9C -> 0x9c
    '\x9d'      #  0x9D -> 0x9d
    '\x9e'      #  0x9E -> 0x9e
    '\x9f'      #  0x9F -> 0x9f
    '\xa0'      #  0xA0 -> 0xa0
    '\u0102'    #  0xA1 -> Ă
    '\xc2'      #  0xA2 -> Â
    '\xca'      #  0xA3 -> Ê
    '\xd4'      #  0xA4 -> Ô
    '\u01a0'    #  0xA5 -> Ơ
    '\u01af'    #  0xA6 -> Ư
    '\u0110'    #  0xA7 -> Đ
    '\u0103'    #  0xA8 -> ă
    '\xe2'      #  0xA9 -> â
    '\xea'      #  0xAA -> ê
    '\xf4'      #  0xAB -> ô
    '\u01a1'    #  0xAC -> ơ
    '\u01b0'    #  0xAD -> ư
    '\u0111'    #  0xAE -> đ
    '\xaf'      #  0xAF -> 0xaf
    '\xb0'      #  0xB0 -> 0xb0
    '\xb1'      #  0xB1 -> 0xb1
    '\xb2'      #  0xB2 -> 0xb2
    '\xb3'      #  0xB3 -> 0xb3
    '\xb4'      #  0xB4 -> 0xb4
    '\xe0'      #  0xB5 -> à
    '\u1ea3'    #  0xB6 -> ả
    '\xe3'      #  0xB7 -> ã
    '\xe1'      #  0xB8 -> á
    '\u1ea1'    #  0xB9 -> ạ
    '\xba'      #  0xBA -> 0xba
    '\u1eb1'    #  0xBB -> ằ
    '\u1eb3'    #  0xBC -> ẳ
    '\u1eb5'    #  0xBD -> ẵ
    '\u1eaf'    #  0xBE -> ắ
    '\xbf'      #  0xBF -> 0xbf
    '\xc0'      #  0xC0 -> 0xc0
    '\xc1'      #  0xC1 -> 0xc1
    '\xc2'      #  0xC2 -> 0xc2
    '\xc3'      #  0xC3 -> 0xc3
    '\xc4'      #  0xC4 -> 0xc4
    '\xc5'      #  0xC5 -> 0xc5
    '\u1eb7'    #  0xC6 -> ặ
    '\u1ea7'    #  0xC7 -> ầ
    '\u1ea9'    #  0xC8 -> ẩ
    '\u1eab'    #  0xC9 -> ẫ
    '\u1ea5'    #  0xCA -> ấ
    '\u1ead'    #  0xCB -> ậ
    '\xe8'      #  0xCC -> è
    '\xcd'      #  0xCD -> 0xcd
    '\u1ebb'    #  0xCE -> ẻ
    '\u1ebd'    #  0xCF -> ẽ
    '\xe9'      #  0xD0 -> é
    '\u1eb9'    #  0xD1 -> ẹ
    '\u1ec1'    #  0xD2 -> ề
    '\u1ec3'    #  0xD3 -> ể
    '\u1ec5'    #  0xD4 -> ễ
    '\u1ebf'    #  0xD5 -> ế
    '\u1ec7'    #  0xD6 -> ệ
    '\xec'      #  0xD7 -> ì
    '\u1ec9'    #  0xD8 -> ỉ
    '\xd9'      #  0xD9 -> 0xd9
    '\xda'      #  0xDA -> 0xda
    '\xdb'      #  0xDB -> 0xdb
    '\u0129'    #  0xDC -> ĩ
    '\xed'      #  0xDD -> í
    '\u1ecb'    #  0xDE -> ị
    '\xf2'      #  0xDF -> ò
    '\xe0'      #  0xE0 -> 0xe0
    '\u1ecf'    #  0xE1 -> ỏ
    '\xf5'      #  0xE2 -> õ
    '\xf3'      #  0xE3 -> ó
    '\u1ecd'    #  0xE4 -> ọ
    '\u1ed3'    #  0xE5 -> ồ
    '\u1ed5'    #  0xE6 -> ổ
    '\u1ed7'    #  0xE7 -> ỗ
    '\u1ed1'    #  0xE8 -> ố
    '\u1ed9'    #  0xE9 -> ộ
    '\u1edd'    #  0xEA -> ờ
    '\u1edf'    #  0xEB -> ở
    '\u1ee1'    #  0xEC -> ỡ
    '\u1edb'    #  0xED -> ớ
    '\u1ee3'    #  0xEE -> ợ
    '\xf9'      #  0xEF -> ù
    '\xf0'      #  0xF0 -> 0xf0
    '\u1ee7'    #  0xF1 -> ủ
    '\u0169'    #  0xF2 -> ũ
    '\xfa'      #  0xF3 -> ú
    '\u1ee5'    #  0xF4 -> ụ
    '\u1eeb'    #  0xF5 -> ừ
    '\u1eed'    #  0xF6 -> ử
    '\u1eef'    #  0xF7 -> ữ
    '\u1ee9'    #  0xF8 -> ứ
    '\u1ef1'    #  0xF9 -> ự
    '\u1ef3'    #  0xFA -> ỳ
    '\u1ef7'    #  0xFB -> ỷ
    '\u1ef9'    #  0xFC -> ỹ
    '\xfd'      #  0xFD -> ý
    '\u1ef5'    #  0xFE -> ỵ
    '\xff'
)

### Encoding table
encoding_table=codecs.charmap_build(decoding_table)

