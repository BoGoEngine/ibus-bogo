#!/usr/bin/env python3.2
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
        self.__id = 0
        engine_name = "BoGo Engine"
        self.__component = \
          IBus.Component.new("org.freedesktop.IBus.BoGoPython",
                             "BoGo Engine for IBus",
                             "0.2",
                             "GPLv3",
                             "Long T. Dam <longdt90@gmail.com>",
                             "https://github.com/BoGoEngine/ibus-bogo-python",
                             "/usr/bin/exec",
                             "ibus-bogo")
        engine = IBus.EngineDesc(name = "bogo-python",
                                longname = engine_name,
                                description = "BoGo Engine for IBus",
                                language = "vi",
                                license = "GPLv3",
                                author = "Long T. Dam <longdt90@gmail.com>",
                                icon = current_path + "/data/ibus-bogo.svg",
                                #icon = "ibus-bogo",
                                layout = "us")
        self.__component.add_engine(engine)
        self.__mainloop = GObject.MainLoop()
        self.__bus = IBus.Bus()
        self.__bus.connect("disconnected", self.__bus_disconnected_cb)
        self.__factory = IBus.Factory.new(self.__bus.get_connection())
        self.__factory.add_engine("bogo-python",
                GObject.type_from_name("EngineBoGo"))
        if exec_by_ibus:
            self.__bus.request_name("org.freedesktop.IBus.BoGoPython", 0)
        else:
            self.__bus.register_component(self.__component)
            self.__bus.set_global_engine_async(
                    "bogo-python", -1, None, None, None)

    def run(self):
        self.__mainloop.run()

    def __bus_disconnected_cb(self, bus):
        self.__mainloop.quit()


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
