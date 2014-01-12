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

from gi.repository import Gio, GObject
from base_config import BaseConfig
import os
import logging


_dirname = os.path.expanduser("~/.config/ibus-bogo/")
if not os.path.exists(_dirname):
    os.makedirs(_dirname)
config_path = os.path.join(_dirname, "config.json")


class Config(BaseConfig, GObject.GObject):
    """Config object, will auto reload."""

    def __init__(self):
        BaseConfig.__init__(self, config_path)
        # GObject.GObject.__init__()

        # TODO: Gio's monitoring is a bit slow
        f = Gio.File.new_for_path(config_path)
        self.monitor = f.monitor_file(0, None)
        self.monitor.connect("changed", self._on_file_changed)

    def _on_file_changed(self, monitor, file, other_file, event_type):
        if event_type == Gio.FileMonitorEvent.CHANGES_DONE_HINT:
            logging.debug("Setting file changed")
            self.read_config(self.path)
