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

import os
import logging
import subprocess


class FocusTracker():

    def __init__(self):
        self.focused_exe = ""

    def on_focus_changed(self):
        focused_pid = subprocess.check_output("xprop -id $(xprop -root | awk '/_NET_ACTIVE_WINDOW\(WINDOW\)/{print $NF}') | awk '/_NET_WM_PID\(CARDINAL\)/{print $NF}'", shell=True).decode().strip()
        os.path.realpath("/proc/{0}/exe".format(focused_pid))
        print(self.focused_exe)

    def is_in_unity_dash(self):
        return self.focused_exe.find("compiz") != -1

    def is_in_firefox(self):
        return self.focused_exe.find("firefox") != -1

    def is_in_chrome(self):
        return self.focused_exe.find("chrome") != -1 \
            or self.focused_exe.find("chromium") != -1

