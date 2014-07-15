BoGo
====

[![Build Status](https://travis-ci.org/BoGoEngine/bogo-python.svg?branch=master)](https://travis-ci.org/BoGoEngine/bogo-python)
[![Coverage Status](https://coveralls.io/repos/BoGoEngine/bogo-python/badge.png?branch=master)](https://coveralls.io/r/BoGoEngine/bogo-python?branch=master)

BoGo is a Vietnamese input method conversion library for Python. This library
is intentionally functional with no internal state and side-effect.

Installation
------------

```bash
pip install bogo
```

Usage
-----

```python
>>> import bogo
>>> bogo.process_sequence('meof')
'mèo'
>>> bogo.process_sequence('meo2', rules=bogo.get_vni_definition())
'mèo'
>>> bogo.process_sequence('system')
'system'
>>> bogo.process_sequence('system', skip_non_vietnamese=False)
'sýtem'
```

More help available with:

```python
>>> help(bogo.core)
```

Some functions from `bogo.core` are exported to package toplevel:

- `process_key()`
- `process_sequence()`
- `get_telex_definition()`
- `get_vni_definition()`

BoGo is extensively tested with Python 2.7, Python 3.2 and Python 3.3.

Etymology
---------

BoGo, or more precisely *bộ gõ*, literally means *input method* in Vietnamese.
