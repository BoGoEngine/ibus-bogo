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
    while i < len(input):
        # FIXME Not sure about endianness here
        try:
            twobyte_code = struct.unpack(">H", input[i:i+2])[0]
        except:
            # It's the last byte. Therefore, skip the two-byte thingy.
            twobyte_code = None

        # Sometimes it's an int, sometimes it's a bytes
        onebyte_code = ord(input[i]) if isinstance(input[i], bytes) \
                       else input[i]

        if twobyte_code in map:
            result.append(struct.pack("=H", map[twobyte_code]).decode('utf-16'))
            i += 2
        elif onebyte_code in map:
            result.append(struct.pack("=H", map[onebyte_code]).decode('utf-16'))
            i += 1
        else:
            onebyte_code = onebyte_code if isinstance(onebyte_code, bytes) \
                           else bytes([onebyte_code])
            result.append(onebyte_code.decode('latin-1'))
            i += 1
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

encoding_map = { decoding_map[key]:key for key in decoding_map }
