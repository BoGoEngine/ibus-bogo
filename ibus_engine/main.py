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

from gi.repository import IBus
from gi.repository import GLib
from gi.repository import GObject

import os
import sys
import locale
import logging
import argparse

ENGINE_PATH = os.path.dirname(__file__)
sys.path.append(os.path.abspath(ENGINE_PATH + ".."))
sys.path.append(os.path.abspath(ENGINE_PATH + "../bogo-python"))

from ibus_engine import Engine
from config import Config
from abbr import AbbreviationExpander
from trayicon import TrayIcon


current_path = os.path.dirname(os.path.abspath(__file__))


class IMApp:

    def __init__(self, exec_by_ibus):
        engine_name = "bogo"
        long_engine_name = "BoGo"
        author = "BoGo Development Team <bogoengine-dev@googlegroups.com>"
        description = "ibus-bogo for IBus"
        version = "0.4"
        license = "GPLv3"

        self.component = \
            IBus.Component.new("org.freedesktop.IBus.BoGo",
                               description,
                               version,
                               license,
                               author,
                               "https://github.com/BoGoEngine/ibus-bogo",
                               "/usr/bin/exec",
                               "ibus-bogo")

        engine = IBus.EngineDesc(name=engine_name,
                                 longname=long_engine_name,
                                 description=description,
                                 language="vi",
                                 license=license,
                                 author=author,
                                 icon=current_path + "/data/ibus-bogo-dev.svg",
                                 # icon = "ibus-bogo",
                                 layout="default")

        self.component.add_engine(engine)
        self.mainloop = GObject.MainLoop()
        self.bus = IBus.Bus()
        self.bus.connect("disconnected", self.bus_disconnected_cb)

        self.engine_count = 0
        self.factory = IBus.Factory.new(self.bus.get_connection())
        self.factory.connect("create-engine", self.create_engine)

        CONFIG_DIR = os.path.expanduser("~/.config/ibus-bogo/")
        self.config = Config()
        self.abbr_expander = AbbreviationExpander(config=self.config)
        self.abbr_expander.watch_file(CONFIG_DIR + "/abbr_rules.json")
        self.icon = TrayIcon()

        if exec_by_ibus:
            self.bus.request_name("org.freedesktop.IBus.BoGo", 0)
        else:
            self.bus.register_component(self.component)
            self.bus.set_global_engine_async(
                "bogo", -1, None, None, None)

    def create_engine(self, factory, engine_name):
        if engine_name == "bogo":
            dbus_path = "/org/freedesktop/IBus/Engine/%d" % self.engine_count

            # It looks like the GObject's new_with_type constructor also
            # calls __init__ but without arguments so there will be error
            # messages like this:
            #
            # TypeError: __init__() missing 1 required positional argument
            #
            # We will ignore that message by temporarily redirect stderr
            # to /dev/null

            f = open('/dev/null', 'w')
            stderr = sys.stderr
            sys.stderr = f

            engine = Engine.new_with_type(GObject.type_from_name("EngineBoGo"),
                                          "bogo-python",
                                          dbus_path,
                                          self.bus.get_connection())

            sys.stderr = stderr
            f.close()

            Engine.__init__(engine, self.config, self.abbr_expander, self.icon)

            self.engine_count += 1
            return engine

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
