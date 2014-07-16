# -*- coding: utf-8 -*-

"""\
BoGo is a Vietnamese input method conversion library. This library
is intentionally functional with no internal state and side-effect.

Usage
-----

>>> import bogo
>>> bogo.process_sequence('meof')
'mèo'
>>> bogo.process_sequence('meo2', rules=bogo.get_vni_definition())
'mèo'
```

Some functions from `bogo.core` are exported to package toplevel:

    - process_key()
    - process_sequence()
    - get_telex_definition()
    - get_vni_definition()

Read `help(bogo.core)` for more help.
"""

from bogo.core import \
    process_key, \
    process_sequence, \
    get_telex_definition, \
    get_vni_definition
