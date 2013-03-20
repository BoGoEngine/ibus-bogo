""" Python Character Mapping Codec tcvn3 generated from 'charset-data/TCVN3.txt' with gencodec.py.

"""#"

import codecs
import json
import os
from . import base_charset


tcvn3 = json.loads(
    open(
        os.path.join(os.path.dirname(__file__),
        "charset-data",
        "TCVN3.json")
    ).read()
)


### encodings module API

def getregentry():
    encode, decode, incre_encode, incre_decode = base_charset.make_charmap_codec(tcvn3)
    return codecs.CodecInfo(
        name='tcvn3',
        encode=encode,
        decode=decode,
        incrementalencoder=incre_encode,
        incrementaldecoder=incre_decode
    )
