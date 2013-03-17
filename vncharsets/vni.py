""" Python Character Mapping Codec vni generated from 'charset-data/VNI.txt' with gencodec.py.

"""#"

import codecs
import struct

### Codec APIs

class Codec(codecs.Codec):

    def encode(self,input,errors='strict'):
        # return codecs.charmap_encode(input,errors,encoding_map)
        return vni_encode(input,errors,encoding_map)

    def decode(self,input,errors='strict'):
        # return codecs.charmap_decode(input,errors,decoding_map)
        return vni_decode(input,errors,decoding_map)


class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final=False):
        # return codecs.charmap_encode(input,self.errors,encoding_map)[0]
        return vni_encode(input,self.errors,encoding_map)[0]


class IncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input, final=False):
        # return codecs.charmap_decode(input,self.errors,decoding_map)[0]
        return vni_decode(input,self.errors,decoding_map)[0]


class StreamWriter(Codec,codecs.StreamWriter):
    pass


class StreamReader(Codec,codecs.StreamReader):
    pass


def vni_encode(input, error, map):
    result = []
    for char in input:
        code_point = ord(char)
        if code_point in map:
            result += int_to_bytes(map[code_point])
        elif 0 < code_point < 0x80:
            result.append(code_point)
    return (bytes(result), len(input))


def vni_decode(input, error, map):
    i = 0
    # len == 1?
    result = []
    # Read a two-byte chunk, if it is in the map, then convert it into utf-8
    # else check if the first byte is in the map, else interpret it as a normal
    # utf-8 char. Continue.
    while i < len(input) - 1:
        twobyte_code = struct.unpack(">H", input[i:i+2])[0]
        onebyte_code = input[i]
        if twobyte_code in map:
            result.append(struct.pack("=H", map[twobyte_code]).decode('utf-16'))
            i += 2
        elif onebyte_code in map:
            result.append(struct.pack("=H", map[onebyte_code]).decode('utf-16'))
            i += 1
        else:
            result.append(input[i:i+1].decode('utf-8'))
            i += 1
    # Read the last byte
    result.append(input[i:i+1].decode('utf-8'))
    return ("".join(result), len(input))


def int_to_bytes(val):
    bytes = []
    while val > 0:
        bytes.append(val & 0xFF)
        val = val >> 8
    return reversed(bytes)


### encodings module API


def getregentry():
    return codecs.CodecInfo(
        name='vni',
        encode=Codec().encode,
        decode=Codec().decode,
        incrementalencoder=IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
        streamreader=StreamReader,
        streamwriter=StreamWriter,
    )


### Decoding Map

decoding_map = {
    0x00: 0x0000,       #  CONTROL CHARACTER
    0x01: 0x0001,       #  CONTROL CHARACTER
    0x02: 0x0002,       #  CONTROL CHARACTER
    0x03: 0x0003,       #  CONTROL CHARACTER
    0x04: 0x0004,       #  CONTROL CHARACTER
    0x05: 0x0005,       #  CONTROL CHARACTER
    0x06: 0x0006,       #  CONTROL CHARACTER
    0x07: 0x0007,       #  CONTROL CHARACTER
    0x08: 0x0008,       #  CONTROL CHARACTER
    0x09: 0x0009,       #  CONTROL CHARACTER
    0x0A: 0x000A,       #  CONTROL CHARACTER
    0x0B: 0x000B,       #  CONTROL CHARACTER
    0x0C: 0x000C,       #  CONTROL CHARACTER
    0x0D: 0x000D,       #  CONTROL CHARACTER
    0x0E: 0x000E,       #  CONTROL CHARACTER
    0x0F: 0x000F,       #  CONTROL CHARACTER
    0x10: 0x0010,       #  CONTROL CHARACTER
    0x11: 0x0011,       #  CONTROL CHARACTER
    0x12: 0x0012,       #  CONTROL CHARACTER
    0x13: 0x0013,       #  CONTROL CHARACTER
    0x14: 0x0014,       #  CONTROL CHARACTER
    0x15: 0x0015,       #  CONTROL CHARACTER
    0x16: 0x0016,       #  CONTROL CHARACTER
    0x17: 0x0017,       #  CONTROL CHARACTER
    0x18: 0x0018,       #  CONTROL CHARACTER
    0x19: 0x0019,       #  CONTROL CHARACTER
    0x1A: 0x001A,       #  CONTROL CHARACTER
    0x1B: 0x001B,       #  CONTROL CHARACTER
    0x1C: 0x001C,       #  CONTROL CHARACTER
    0x1D: 0x001D,       #  CONTROL CHARACTER
    0x1E: 0x001E,       #  CONTROL CHARACTER
    0x1F: 0x001F,       #  CONTROL CHARACTER
    0x7F: 0x007F,       #  CONTROL CHARACTER
    0xC6: 0x1EC8,       #  Ỉ
    0xCC: 0x00CC,       #  Ì
    0xCD: 0x00CD,       #  Í
    0xCE: 0x1EF4,       #  Ỵ
    0xD1: 0x0110,       #  Đ
    0xD2: 0x1ECA,       #  Ị
    0xD3: 0x0128,       #  Ĩ
    0xD4: 0x01A0,       #  Ơ
    0xD6: 0x01AF,       #  Ư
    0xE6: 0x1EC9,       #  ỉ
    0xEC: 0x00EC,       #  ì
    0xED: 0x00ED,       #  í
    0xEE: 0x1EF5,       #  ỵ
    0xF1: 0x0111,       #  đ
    0xF2: 0x1ECB,       #  ị
    0xF3: 0x0129,       #  ĩ
    0xF4: 0x01A1,       #  ơ
    0xF6: 0x01B0,       #  ư
    0xFF: 0x00FF,
    0x41C0: 0x1EA6,     #  Ầ
    0x41C1: 0x1EA4,     #  Ấ
    0x41C2: 0x00C2,     #  Â
    0x41C3: 0x1EAA,     #  Ẫ
    0x41C4: 0x1EAC,     #  Ậ
    0x41C5: 0x1EA8,     #  Ẩ
    0x41C8: 0x1EB0,     #  Ằ
    0x41C9: 0x1EAE,     #  Ắ
    0x41CA: 0x0102,     #  Ă
    0x41CB: 0x1EB6,     #  Ặ
    0x41CF: 0x1EA0,     #  Ạ
    0x41D5: 0x00C3,     #  Ã
    0x41D8: 0x00C0,     #  À
    0x41D9: 0x00C1,     #  Á
    0x41DA: 0x1EB2,     #  Ẳ
    0x41DB: 0x1EA2,     #  Ả
    0x41DC: 0x1EB4,     #  Ẵ
    0x45C0: 0x1EC0,     #  Ề
    0x45C1: 0x1EBE,     #  Ế
    0x45C2: 0x00CA,     #  Ê
    0x45C3: 0x1EC4,     #  Ễ
    0x45C4: 0x1EC6,     #  Ệ
    0x45C5: 0x1EC2,     #  Ể
    0x45CF: 0x1EB8,     #  Ẹ
    0x45D5: 0x1EBC,     #  Ẽ
    0x45D8: 0x00C8,     #  È
    0x45D9: 0x00C9,     #  É
    0x45DB: 0x1EBA,     #  Ẻ
    0x4FC0: 0x1ED2,     #  Ồ
    0x4FC1: 0x1ED0,     #  Ố
    0x4FC2: 0x00D4,     #  Ô
    0x4FC3: 0x1ED6,     #  Ỗ
    0x4FC4: 0x1ED8,     #  Ộ
    0x4FC5: 0x1ED4,     #  Ổ
    0x4FCF: 0x1ECC,     #  Ọ
    0x4FD5: 0x00D5,     #  Õ
    0x4FD8: 0x00D2,     #  Ò
    0x4FD9: 0x00D3,     #  Ó
    0x4FDB: 0x1ECE,     #  Ỏ
    0x55CF: 0x1EE4,     #  Ụ
    0x55D5: 0x0168,     #  Ũ
    0x55D8: 0x00D9,     #  Ù
    0x55D9: 0x00DA,     #  Ú
    0x55DB: 0x1EE6,     #  Ủ
    0x59D5: 0x1EF8,     #  Ỹ
    0x59D8: 0x1EF2,     #  Ỳ
    0x59D9: 0x00DD,     #  Ý
    0x59DB: 0x1EF6,     #  Ỷ
    0x61E0: 0x1EA7,     #  ầ
    0x61E1: 0x1EA5,     #  ấ
    0x61E2: 0x00E2,     #  â
    0x61E3: 0x1EAB,     #  ẫ
    0x61E4: 0x1EAD,     #  ậ
    0x61E5: 0x1EA9,     #  ẩ
    0x61E8: 0x1EB1,     #  ằ
    0x61E9: 0x1EAF,     #  ắ
    0x61EA: 0x0103,     #  ă
    0x61EB: 0x1EB7,     #  ặ
    0x61EF: 0x1EA1,     #  ạ
    0x61F5: 0x00E3,     #  ã
    0x61F8: 0x00E0,     #  à
    0x61F9: 0x00E1,     #  á
    0x61FA: 0x1EB3,     #  ẳ
    0x61FB: 0x1EA3,     #  ả
    0x61FC: 0x1EB5,     #  ẵ
    0x65E0: 0x1EC1,     #  ề
    0x65E1: 0x1EBF,     #  ế
    0x65E2: 0x00EA,     #  ê
    0x65E3: 0x1EC5,     #  ễ
    0x65E4: 0x1EC7,     #  ệ
    0x65E5: 0x1EC3,     #  ể
    0x65EF: 0x1EB9,     #  ẹ
    0x65F5: 0x1EBD,     #  ẽ
    0x65F8: 0x00E8,     #  è
    0x65F9: 0x00E9,     #  é
    0x65FB: 0x1EBB,     #  ẻ
    0x6FE0: 0x1ED3,     #  ồ
    0x6FE1: 0x1ED1,     #  ố
    0x6FE2: 0x00F4,     #  ô
    0x6FE3: 0x1ED7,     #  ỗ
    0x6FE4: 0x1ED9,     #  ộ
    0x6FE5: 0x1ED5,     #  ổ
    0x6FEF: 0x1ECD,     #  ọ
    0x6FF5: 0x00F5,     #  õ
    0x6FF8: 0x00F2,     #  ò
    0x6FF9: 0x00F3,     #  ó
    0x6FFB: 0x1ECF,     #  ỏ
    0x75EF: 0x1EE5,     #  ụ
    0x75F5: 0x0169,     #  ũ
    0x75F8: 0x00F9,     #  ù
    0x75F9: 0x00FA,     #  ú
    0x75FB: 0x1EE7,     #  ủ
    0x79F5: 0x1EF9,     #  ỹ
    0x79F8: 0x1EF3,     #  ỳ
    0x79F9: 0x00FD,     #  ý
    0x79FB: 0x1EF7,     #  ỷ
    0xD4CF: 0x1EE2,     #  Ợ
    0xD4D5: 0x1EE0,     #  Ỡ
    0xD4D8: 0x1EDC,     #  Ờ
    0xD4D9: 0x1EDA,     #  Ớ
    0xD4DB: 0x1EDE,     #  Ở
    0xD6CF: 0x1EF0,     #  Ự
    0xD6D5: 0x1EEE,     #  Ữ
    0xD6D8: 0x1EEA,     #  Ừ
    0xD6D9: 0x1EE8,     #  Ứ
    0xD6DB: 0x1EEC,     #  Ử
    0xF4EF: 0x1EE3,     #  ợ
    0xF4F5: 0x1EE1,     #  ỡ
    0xF4F8: 0x1EDD,     #  ờ
    0xF4F9: 0x1EDB,     #  ớ
    0xF4FB: 0x1EDF,     #  ở
    0xF6EF: 0x1EF1,     #  ự
    0xF6F5: 0x1EEF,     #  ữ
    0xF6F8: 0x1EEB,     #  ừ
    0xF6F9: 0x1EE9,     #  ứ
    0xF6FB: 0x1EED,     #  ử
}

### Encoding Map

encoding_map = {
    0x0000: 0x00,       #  CONTROL CHARACTER
    0x0001: 0x01,       #  CONTROL CHARACTER
    0x0002: 0x02,       #  CONTROL CHARACTER
    0x0003: 0x03,       #  CONTROL CHARACTER
    0x0004: 0x04,       #  CONTROL CHARACTER
    0x0005: 0x05,       #  CONTROL CHARACTER
    0x0006: 0x06,       #  CONTROL CHARACTER
    0x0007: 0x07,       #  CONTROL CHARACTER
    0x0008: 0x08,       #  CONTROL CHARACTER
    0x0009: 0x09,       #  CONTROL CHARACTER
    0x000A: 0x0A,       #  CONTROL CHARACTER
    0x000B: 0x0B,       #  CONTROL CHARACTER
    0x000C: 0x0C,       #  CONTROL CHARACTER
    0x000D: 0x0D,       #  CONTROL CHARACTER
    0x000E: 0x0E,       #  CONTROL CHARACTER
    0x000F: 0x0F,       #  CONTROL CHARACTER
    0x0010: 0x10,       #  CONTROL CHARACTER
    0x0011: 0x11,       #  CONTROL CHARACTER
    0x0012: 0x12,       #  CONTROL CHARACTER
    0x0013: 0x13,       #  CONTROL CHARACTER
    0x0014: 0x14,       #  CONTROL CHARACTER
    0x0015: 0x15,       #  CONTROL CHARACTER
    0x0016: 0x16,       #  CONTROL CHARACTER
    0x0017: 0x17,       #  CONTROL CHARACTER
    0x0018: 0x18,       #  CONTROL CHARACTER
    0x0019: 0x19,       #  CONTROL CHARACTER
    0x001A: 0x1A,       #  CONTROL CHARACTER
    0x001B: 0x1B,       #  CONTROL CHARACTER
    0x001C: 0x1C,       #  CONTROL CHARACTER
    0x001D: 0x1D,       #  CONTROL CHARACTER
    0x001E: 0x1E,       #  CONTROL CHARACTER
    0x001F: 0x1F,       #  CONTROL CHARACTER
    0x007F: 0x7F,       #  CONTROL CHARACTER
    0x00C0: 0x41D8,     #  À
    0x00C1: 0x41D9,     #  Á
    0x00C2: 0x41C2,     #  Â
    0x00C3: 0x41D5,     #  Ã
    0x00C8: 0x45D8,     #  È
    0x00C9: 0x45D9,     #  É
    0x00CA: 0x45C2,     #  Ê
    0x00CC: 0xCC,       #  Ì
    0x00CD: 0xCD,       #  Í
    0x00D2: 0x4FD8,     #  Ò
    0x00D3: 0x4FD9,     #  Ó
    0x00D4: 0x4FC2,     #  Ô
    0x00D5: 0x4FD5,     #  Õ
    0x00D9: 0x55D8,     #  Ù
    0x00DA: 0x55D9,     #  Ú
    0x00DD: 0x59D9,     #  Ý
    0x00E0: 0x61F8,     #  à
    0x00E1: 0x61F9,     #  á
    0x00E2: 0x61E2,     #  â
    0x00E3: 0x61F5,     #  ã
    0x00E8: 0x65F8,     #  è
    0x00E9: 0x65F9,     #  é
    0x00EA: 0x65E2,     #  ê
    0x00EC: 0xEC,       #  ì
    0x00ED: 0xED,       #  í
    0x00F2: 0x6FF8,     #  ò
    0x00F3: 0x6FF9,     #  ó
    0x00F4: 0x6FE2,     #  ô
    0x00F5: 0x6FF5,     #  õ
    0x00F9: 0x75F8,     #  ù
    0x00FA: 0x75F9,     #  ú
    0x00FD: 0x79F9,     #  ý
    0x00FF: 0xFF,
    0x0102: 0x41CA,     #  Ă
    0x0103: 0x61EA,     #  ă
    0x0110: 0xD1,       #  Đ
    0x0111: 0xF1,       #  đ
    0x0128: 0xD3,       #  Ĩ
    0x0129: 0xF3,       #  ĩ
    0x0168: 0x55D5,     #  Ũ
    0x0169: 0x75F5,     #  ũ
    0x01A0: 0xD4,       #  Ơ
    0x01A1: 0xF4,       #  ơ
    0x01AF: 0xD6,       #  Ư
    0x01B0: 0xF6,       #  ư
    0x1EA0: 0x41CF,     #  Ạ
    0x1EA1: 0x61EF,     #  ạ
    0x1EA2: 0x41DB,     #  Ả
    0x1EA3: 0x61FB,     #  ả
    0x1EA4: 0x41C1,     #  Ấ
    0x1EA5: 0x61E1,     #  ấ
    0x1EA6: 0x41C0,     #  Ầ
    0x1EA7: 0x61E0,     #  ầ
    0x1EA8: 0x41C5,     #  Ẩ
    0x1EA9: 0x61E5,     #  ẩ
    0x1EAA: 0x41C3,     #  Ẫ
    0x1EAB: 0x61E3,     #  ẫ
    0x1EAC: 0x41C4,     #  Ậ
    0x1EAD: 0x61E4,     #  ậ
    0x1EAE: 0x41C9,     #  Ắ
    0x1EAF: 0x61E9,     #  ắ
    0x1EB0: 0x41C8,     #  Ằ
    0x1EB1: 0x61E8,     #  ằ
    0x1EB2: 0x41DA,     #  Ẳ
    0x1EB3: 0x61FA,     #  ẳ
    0x1EB4: 0x41DC,     #  Ẵ
    0x1EB5: 0x61FC,     #  ẵ
    0x1EB6: 0x41CB,     #  Ặ
    0x1EB7: 0x61EB,     #  ặ
    0x1EB8: 0x45CF,     #  Ẹ
    0x1EB9: 0x65EF,     #  ẹ
    0x1EBA: 0x45DB,     #  Ẻ
    0x1EBB: 0x65FB,     #  ẻ
    0x1EBC: 0x45D5,     #  Ẽ
    0x1EBD: 0x65F5,     #  ẽ
    0x1EBE: 0x45C1,     #  Ế
    0x1EBF: 0x65E1,     #  ế
    0x1EC0: 0x45C0,     #  Ề
    0x1EC1: 0x65E0,     #  ề
    0x1EC2: 0x45C5,     #  Ể
    0x1EC3: 0x65E5,     #  ể
    0x1EC4: 0x45C3,     #  Ễ
    0x1EC5: 0x65E3,     #  ễ
    0x1EC6: 0x45C4,     #  Ệ
    0x1EC7: 0x65E4,     #  ệ
    0x1EC8: 0xC6,       #  Ỉ
    0x1EC9: 0xE6,       #  ỉ
    0x1ECA: 0xD2,       #  Ị
    0x1ECB: 0xF2,       #  ị
    0x1ECC: 0x4FCF,     #  Ọ
    0x1ECD: 0x6FEF,     #  ọ
    0x1ECE: 0x4FDB,     #  Ỏ
    0x1ECF: 0x6FFB,     #  ỏ
    0x1ED0: 0x4FC1,     #  Ố
    0x1ED1: 0x6FE1,     #  ố
    0x1ED2: 0x4FC0,     #  Ồ
    0x1ED3: 0x6FE0,     #  ồ
    0x1ED4: 0x4FC5,     #  Ổ
    0x1ED5: 0x6FE5,     #  ổ
    0x1ED6: 0x4FC3,     #  Ỗ
    0x1ED7: 0x6FE3,     #  ỗ
    0x1ED8: 0x4FC4,     #  Ộ
    0x1ED9: 0x6FE4,     #  ộ
    0x1EDA: 0xD4D9,     #  Ớ
    0x1EDB: 0xF4F9,     #  ớ
    0x1EDC: 0xD4D8,     #  Ờ
    0x1EDD: 0xF4F8,     #  ờ
    0x1EDE: 0xD4DB,     #  Ở
    0x1EDF: 0xF4FB,     #  ở
    0x1EE0: 0xD4D5,     #  Ỡ
    0x1EE1: 0xF4F5,     #  ỡ
    0x1EE2: 0xD4CF,     #  Ợ
    0x1EE3: 0xF4EF,     #  ợ
    0x1EE4: 0x55CF,     #  Ụ
    0x1EE5: 0x75EF,     #  ụ
    0x1EE6: 0x55DB,     #  Ủ
    0x1EE7: 0x75FB,     #  ủ
    0x1EE8: 0xD6D9,     #  Ứ
    0x1EE9: 0xF6F9,     #  ứ
    0x1EEA: 0xD6D8,     #  Ừ
    0x1EEB: 0xF6F8,     #  ừ
    0x1EEC: 0xD6DB,     #  Ử
    0x1EED: 0xF6FB,     #  ử
    0x1EEE: 0xD6D5,     #  Ữ
    0x1EEF: 0xF6F5,     #  ữ
    0x1EF0: 0xD6CF,     #  Ự
    0x1EF1: 0xF6EF,     #  ự
    0x1EF2: 0x59D8,     #  Ỳ
    0x1EF3: 0x79F8,     #  ỳ
    0x1EF4: 0xCE,       #  Ỵ
    0x1EF5: 0xEE,       #  ỵ
    0x1EF6: 0x59DB,     #  Ỷ
    0x1EF7: 0x79FB,     #  ỷ
    0x1EF8: 0x59D5,     #  Ỹ
    0x1EF9: 0x79F5,     #  ỹ
}
