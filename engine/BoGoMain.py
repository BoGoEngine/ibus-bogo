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
import getopt
import locale

from BoGoEngine import Engine

class IMApp:
    def __init__(self, exec_by_ibus, charset):
        engine_name = "Bogo Engine (" + charset +")"
        self.__component = \
                IBus.Component.new("org.freedesktop.IBus.BoGoPython",
                                   "BoGo Python Component",
                                   "0.1.0",
                                   "GPLv3",
                                   "Long T. Dam <longdt90@gmail.com>",
                                   "http://example.com",
                                   "/usr/bin/exec",
                                   "ibus-bogo")
        engine = IBus.EngineDesc.new("bogo-python",
                                     engine_name,
                                     "English BoGo",
                                     "vi",
                                     "GPLv3",
                                     "Long T. Dam <longdt90@gmail.com>",
                                     "",
                                     "us")
        self.__component.add_engine(engine)
        self.__mainloop = GLib.MainLoop()
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


def launch_engine(exec_by_ibus, charset):
    IBus.init()
    IMApp(exec_by_ibus, charset).run()

def print_help(out, v = 0):
    print >> out, "-i, --ibus             executed by IBus."
    print >> out, "-h, --help             show this message."
    print >> out, "-d, --daemonize        daemonize ibus"
    print >> out, "-u, --utf8             use UTF8 charset"
    print >> out, "-t, --tcvn3            use TCVN3 charset"
    sys.exit(v)

def main():
    try:
        locale.setlocale(locale.LC_ALL, "")
    except:
        pass

    exec_by_ibus = False
    daemonize = False
    charset = "UTF8"

    shortopt = "ihdut"
    longopt = ["ibus", "help", "daemonize", "utf8", "tcvn3"]

    try:
        opts, args = getopt.getopt(sys.argv[1:], shortopt, longopt)
    except getopt.GetoptError, err:
        print_help(sys.stderr, 1)

    for o, a in opts:
        if o in ("-h", "--help"):
            print_help(sys.stdout)
        elif o in ("-d", "--daemonize"):
            daemonize = True
        elif o in ("-i", "--ibus"):
            exec_by_ibus = True
        elif o in ("-u", "--utf8"):
            charset = "UTF8"
        elif o in ("-t", "--tcvn3"):
            charset = "TCVN3"
        else:
            print >> sys.stderr, "Unknown argument: %s" % o
            print_help(sys.stderr, 1)

    if daemonize:
        if os.fork():
            sys.exit()

    launch_engine(exec_by_ibus,charset)

if __name__ == "__main__":
    main()
