#
# This file is part of ibus-bogo project.
#
# Copyright (C) 2012 Long T. Dam <longdt90@gmail.com>
# Copyright (C) 2012-2013 Trung Ngo <ndtrung4419@gmail.com>
# Copyright (C) 2013 Duong H. Nguyen <cmpitg@gmail.com>
#
# ibus-bogo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ibus-bogo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ibus-bogo.  If not, see <http://www.gnu.org/licenses/>.
#

from collections import defaultdict
import logging
import json
import os
import bogo


# TODO: This module needs some tests
ENGINE_DIR = os.path.dirname(__file__)

IBUS_BOGO_DEFAULT_CONFIG = {
    "input-method": "telex",
    "output-charset": "utf-8",
    "telex-w-shorthand": True,
    "telex-brackets-shorthand": True,
    "skip-non-vietnamese": True,
    "enable-text-expansion": False,
    "auto-capitalize-expansion": False,
    "surrounding-text-blacklist": [
        "chrome",
        "chromium",
        "compiz",
        "gnome-terminal",
        "lxterminal",
        "konsole",
        "geany",
        "skype"
    ],
    "typo-correction-level": 2,
    "typo-correction-threshold": 2
}


# TODO: It's best if we can preserve comments and line order
class BaseConfig(object):
    """Base config object, designed to behave like a dictionary.
    """

    def __init__(self, path):
        super(BaseConfig, self).__init__()
        self._keys = {}
        self.path = path
        self.read_default_config()
        self.read_config(path)

        # Write immediately because the default config
        # may introduce a new key
        self.write_config()

    def read_config(self, path):
        try:
            f = open(path, "r")
            data = json.loads(f.read())
            self._keys.update(data)
            f.close()
        except:
            logging.warning("Config file corrupted or doesn't exist.")
            self.reset()
        finally:
            # FIXME: What is this code for?
            tmp = self._keys
            self._keys.update(tmp)

    def write_config(self):
        f = open(self.path, "w")
        f.write(json.dumps(self._keys,
                           indent=4,
                           ensure_ascii=False,
                           sort_keys=True))
        f.close()

    def __setitem__(self, key, value):
        self._keys[key] = value
        self.write_config()

    def __getitem__(self, key):
        if key == "input-method-definition":
            return defaultdict(dict, {
                "vni": bogo.get_vni_definition(),
                "telex": bogo.get_telex_definition(
                    self._keys["telex-w-shorthand"],
                    self._keys["telex-brackets-shorthand"])
            })[self._keys["input-method"]]
        else:
            return self._keys[key]

    def __contains__(self, key):
        return self._keys.__contains__(key)

    def items(self):
        return self._keys.items()

    def iteritems(self):
        return self._keys.iteritems()

    def keys(self):
        return self._keys.keys()

    def read_default_config(self):
        self._keys.update(IBUS_BOGO_DEFAULT_CONFIG)

    def reset(self):
        self._keys = {}
        self.read_default_config()
        self.write_config()

