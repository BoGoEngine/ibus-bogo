from functools import partial
import codecs


"""
http://docs.python.org/3/library/codecs.html
"""


# We have to make our own encoder/decoder for charset-based codecs because
# Python's native C codec has a problem with TCVN3's 'à' character (0xb5) and
# French's 'à' character (0xe0) in ISO-8859-1. It always thinks that the
# Unicode 'à' should be mapped to the French one.
# Who knows what else it can do?
# TODO Make this more efficient.


def _charmap_encoder(input, errors="strict", encoding_table=None):
    result = []
    for char in input:
        if char in encoding_table:
            result.append(ord(encoding_table[char]))
        else:
            result.append(ord(char.encode('latin-1')))
    return (bytes(result), len(input))


def _charmap_decoder(input, errors="strict", decoding_table=None):
    result = []
    for byte in input:
        # When invoked as a stateless decoder, `byte`'s type is a "bytes" but
        # when invoked through IncrementalEncoder, `byte` is an int.
        byte = byte if isinstance(byte, bytes) else bytes([byte])
        byte = byte.decode('latin-1')
        if byte in decoding_table:
            result.append(decoding_table[byte])
        else:
            result.append(byte)
    return ("".join(result), len(input))


class _IncrementalEncoder(codecs.IncrementalEncoder):
    def __init__(self, errors="strict", encoding_table=None):
        super(_IncrementalEncoder, self).__init__(errors)
        self.encoding_table = encoding_table

    def encode(self, input, final=False):
        return _charmap_encoder(input, self.errors, self.encoding_table)[0]


class _IncrementalDecoder(codecs.IncrementalDecoder):
    def __init__(self, errors="strict", decoding_table=None):
        super(_IncrementalDecoder, self).__init__(errors)
        self.decoding_table = decoding_table

    def decode(self, input, final=False):
        a = _charmap_decoder(input, self.errors, self.decoding_table)[0]
        return a


def make_charmap_encoder(encoding_table):
    return partial(_charmap_encoder, encoding_table=encoding_table)


def make_charmap_decoder(decoding_table):
    return partial(_charmap_decoder, decoding_table=decoding_table)


def make_incre_encoder(encoding_table):
    return partial(_IncrementalEncoder, encoding_table=encoding_table)


def make_incre_decoder(decoding_table):
    return partial(_IncrementalDecoder, decoding_table=decoding_table)


def make_charmap_codec(charset):
    _decoding_table = charset["table"]
    _encoding_table = {v:k for k, v in _decoding_table.items()}

    return (make_charmap_encoder(_encoding_table),
            make_charmap_decoder(_decoding_table),
            make_incre_encoder(_encoding_table),
            make_incre_decoder(_decoding_table)
            )
