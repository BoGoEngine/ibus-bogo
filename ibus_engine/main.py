#
# This file is part of ibus-bogo-python project.
#
# Copyright (C) 2012 Long T. Dam <longdt90@gmail.com>
# Copyright (C) 2012-2013 Trung Ngo <ndtrung4419@gmail.com>
# Copyright (C) 2013 Duong H. Nguyen <cmpitg@gmail.com>
#
# ibus-bogo-python is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ibus-bogo-python is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ibus-bogo-python.  If not, see <http://www.gnu.org/licenses/>.
#

from gi.repository import IBus
from gi.repository import GLib
from gi.repository import GObject

import os
import sys
import locale
import logging
import argparse

from ibus_engine import Engine


current_path = os.path.dirname(os.path.abspath(__file__))


class IMApp:

    def __init__(self, exec_by_ibus):
        engine_name = "bogo-python"
        long_engine_name = "bogo-python"
        author = "BoGo Development Team <bogoengine-dev@googlegroups.com>"
        description = "ibus-bogo-python for IBus"
        version = "0.3"
        license = "GPLv3"

        self.component = \
            IBus.Component.new("org.freedesktop.IBus.BoGoPython",
                               description,
                               version,
                               license,
                               author,
                               "https://github.com/BoGoEngine/ibus-bogo-python",
                               "/usr/bin/exec",
                               "ibus-bogo")

        engine = IBus.EngineDesc(name=engine_name,
                                 longname=long_engine_name,
                                 description=description,
                                 language="vi",
                                 license=license,
                                 author=author,
                                 icon=current_path + "/data/ibus-bogo.svg",
                                 # icon = "ibus-bogo",
                                 layout="us")

        self.component.add_engine(engine)
        self.mainloop = GObject.MainLoop()
        self.bus = IBus.Bus()
        self.bus.connect("disconnected", self.bus_disconnected_cb)
        self.factory = IBus.Factory.new(self.bus.get_connection())
        self.factory.add_engine(engine_name,
                                GObject.type_from_name("EngineBoGo"))
        if exec_by_ibus:
            self.bus.request_name("org.freedesktop.IBus.BoGoPython", 0)
        else:
            self.bus.register_component(self.component)
            self.bus.set_global_engine_async(
                    "bogo-python", -1, None, None, None)

    def run(self):
        self.mainloop.run()

    def bus_disconnected_cb(self, bus):
        self.mainloop.quit()


def launch_engine(exec_by_ibus):
    IBus.init()
    IMApp(exec_by_ibus).run()


def main():
    try:
        locale.setlocale(locale.LC_ALL, "")
    except:
        pass

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ibus", help="executed by IBus",
                        action="store_true")
    args = parser.parse_args()
    exec_by_ibus = False
    if args.ibus:
        exec_by_ibus = True

    if not exec_by_ibus:
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    launch_engine(exec_by_ibus)


if __name__ == "__main__":
    main()
