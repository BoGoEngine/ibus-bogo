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

import logging
import json
import os
import bogo


# TODO: This module needs some tests
ENGINE_DIR = os.path.dirname(__file__)
DEFAULT_CONFIG_PATH = ENGINE_DIR + "/data/default_config.json"

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

    def read_config(self, path):
        try:
            f = open(path, "r")
            data = json.loads(f.read())
            self._keys.update(data)
            f.close()
        except:
            logging.debug("Config file corrupted or not exists.")
            self.reset()
        finally:
            tmp = self._keys
            self._keys = bogo.default_config.copy()
            self._keys.update(tmp)
            self.sanity_check()

    def write_config(self):
        f = open(self.path, "w")
        f.write(json.dumps(self._keys, indent=4, ensure_ascii=False))
        f.close()

    def __setitem__(self, key, value):
        self._keys[key] = value
        self.write_config()

    def __getitem__(self, key):
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
        self.read_config(DEFAULT_CONFIG_PATH)

    def reset(self):
        # Only reset what's needed
        self.read_default_config()
        self.write_config()

    def sanity_check(self):
        # Should check something here
        if self._keys["input-method"] not in self._keys["default-input-methods"] and \
                "custom-input-methods" in self._keys and \
                self._keys["input-method"] not in self._keys["custom-input-methods"]:
            raise ValueError

