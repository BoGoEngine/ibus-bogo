#
# This file is part of ibus-bogo project.
#
# Copyright (C) 2014 Trung Ngo <ndtrung4419@gmail.com>
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

from gi.repository import Wnck
import os
import logging


class FocusTracker():

    class NoneWindow():
        def get_name(self):
            return ""

        def get_class(self):
            return -1

        def get_class_group_name(self):
            return ""

    def __init__(self):
        self.window = FocusTracker.NoneWindow()

    def on_focus_changed(self):
        screen = Wnck.Screen.get_default()
        screen.force_update()
        active_window = screen.get_active_window()

        if active_window:
            self.window = active_window
        else:
            logging.debug("Can't detect window")
            self.window = FocusTracker.NoneWindow()

    def is_in_unity_dash(self):

        def is_in_unity_desktop():
            try:
                return os.environ["XDG_CURRENT_DESKTOP"] == "Unity"
            except KeyError:
                return False

        if is_in_unity_desktop() and \
                self.window.get_window_type() == Wnck.WindowType.DOCK and \
                self.window.get_name() in ['launcher', 'unity-dash']:
            return True
        else:
            return False

    def is_in_firefox(self):
        return \
            self.window.get_class_group_name() in ["Firefox"]

    def is_in_chrome(self):
        return \
            self.window.get_class_group_name() in ["Google-chrome-unstable"]
