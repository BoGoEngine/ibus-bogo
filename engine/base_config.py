#
# IBus-BoGo - The Vietnamese IME for IBus
#
# Copyright (c) 2012- Long T. Dam <longdt90@gmail.com>,
#                     Trung Ngo <ndtrung4419@gmail.com>
#
# This file is part of IBus-BoGo Project
# IBus-BoGo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# IBus-BoGo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with IBus-BoGo.  If not, see <http://www.gnu.org/licenses/>.


import logging
import json
import os


# TODO: This module needs some tests

engine_dir = os.path.dirname(__file__)


# TODO: It's best if we can preserve comments and line order
class BaseConfig(object):
    """Base config object, designed to behave like a dictionary.
    """

    def __init__(self, path):
        super(BaseConfig, self).__init__()
        self.keys = {}
        self.path = path
        f = open(path, "a")
        f.close()
        self.read_config(path)

    def read_config(self, path):
        try:
            f = open(path, "r")
            data = json.loads(f.read())
            self.keys.update(data)
            f.close()
            self.sanity_check()
        except:
            logging.debug("Config file corrupted or not exists.")
            self.reset()

    def write_config(self):
        f = open(self.path, "w")
        f.write(json.dumps(self.keys, indent=4, ensure_ascii=False))
        f.close()

    def __setitem__(self, key, value):
        self.keys[key] = value
        self.write_config()

    def __getitem__(self, key):
        return self.keys[key]

    def __contains__(self, key):
        return self.keys.__contains__(key)

    def reset(self):
        # Only reset what's needed
        self.read_config(os.path.join(engine_dir, "data", "default_config.json"))
        self.write_config()

    def sanity_check(self):
        # Should check something here
        if self.keys["input-method"] not in self.keys["default-input-methods"] and \
                "custom-input-methods" in self.keys and \
                self.keys["input-method"] not in self.keys["custom-input-methods"]:
            raise ValueError

