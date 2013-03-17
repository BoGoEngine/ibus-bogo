from bogo.bogo import process_key
from base_config import BaseConfig
from functools import partial

c = BaseConfig("/tmp/bogo.json")
c['skip-non-vietnamese'] = True

def process_seq(seq, config=c):
    string = ""
    raw = string
    for i in seq:
        string, raw = process_key(string, i, raw_key_sequence=raw,
                             config=config)
    return string

process_seq_non_vn = partial(process_seq, config=c)

print(process_seq_non_vn('gi[f'))
#print(process_key('hư', 'w', raw_key_sequence='hw', config=c))
#print(process_key('ư', 'w', raw_key_sequence='w', config=c))
