# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='bogo',
    packages=['bogo'],
    version='1.0.1',
    description='Library for implementing Vietnamese input method editors with a purely functional interface.',
    author='Trung Ngo',
    author_email='ndtrung4419@gmail.com',
    url='https://github.com/BoGoEngine/bogo-python',
    download_url='https://github.com/BoGoEngine/bogo-python/archive/v1.0.tar.gz',
    keywords=['vietnamese'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    long_description="""\
BoGo is a Vietnamese input method conversion library. This library
is intentionally functional with no internal state and side-effect.

Usage
-----

>>> import bogo
>>> bogo.process_sequence('meof')
'mèo'
>>> bogo.process_sequence('meo2', rules=bogo.get_vni_definition())
'mèo'
>>> bogo.process_sequence('system')
'system'
>>> bogo.process_sequence('system', skip_non_vietnamese=False)
'sýtem'

More help available with:

>>> help(bogo.core)

Some functions from bogo.core are exported to package toplevel:

- `process_key()`
- `process_sequence()`
- `get_telex_definition()`
- `get_vni_definition()`

BoGo is extensively tested with Python 2.7, Python 3.2 and Python 3.3.
"""

)
