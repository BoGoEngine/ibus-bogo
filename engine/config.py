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

from gi.repository import Gio, GObject
import logging
import json
import os

_dirname = os.path.expanduser("~/.config/ibus-bogo/")
if not os.path.exists(_dirname):
    os.makedirs(_dirname)
config_path = os.path.join(_dirname, "config.json")

class Config(GObject.GObject):
    """Config object, designed to behave like a dictionary. It will auto reload when
    the config file is changed.
    """

    def __init__(self):
        GObject.GObject.__init__(self)

        path = config_path
        self.path = path

        self.hash = {}
        self.read_config()

        # TODO: Gio's monitoring is a bit slow
        f = Gio.File.new_for_path(path)
        self.monitor = f.monitor_file(0, None)
        self.monitor.connect("changed", self.on_settings_changed)

    def on_settings_changed(self, monitor, file, other_file, event_type):
        if event_type == Gio.FileMonitorEvent.CHANGES_DONE_HINT:
            logging.debug("Setting file changed")
            self.read_config()

    def read_config(self):
        f = open(self.path, "r")
        data = json.loads(f.read())
        if self.sanity_check(data):
            for key in data:
                self.hash[key] = data[key]
            f.close()
        else:
            # Default to something pre-configured
            pass

    # def write_config(self):
    #     f = open(self.path, "w")
    #     f.write(json.dumps(self.hash, indent=4))
    #     f.close()

    # def __setitem__(self, key, value):
    #     self.hash[key] = value
    #     self.write_config()

    def __getitem__(self, key):
        return self.hash[key]

    def sanity_check(self, config_object):
        return True
