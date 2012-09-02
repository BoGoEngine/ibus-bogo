# IBus-Bogo - The Vietnamese IME for IBus
#
# Copyright (c) 2012- Long T. Dam <longdt90@gmail.com>
#
# This file is part of IBus-Bogo Project
# IBus-Bogo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with IBus-Bogo.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import getopt
import ibus
import factory
import gobject
import locale

class IMApp:
    def __init__(self, exec_by_ibus):
        self.__component = ibus.Component("org.freedesktop.IBus.BogoPython",
                                          "Bogo Python Component",
                                          "0.1.0",
                                          "GPLv3",
                                          "Long T. Dam <longdt90@gmail.com>")
        self.__component.add_engine("bogo-python",
                                    "bogo python",
                                    "Bogo Engine Python",
                                    "vi",
                                    "GPLv3",
                                    "Long T. Dam <longdt90@gmail.com>",
                                    "",
                                    "en")
        self.__mainloop = gobject.MainLoop()
        self.__bus = ibus.Bus()
        self.__bus.connect("disconnected", self.__bus_disconnected_cb)
        self.__factory = factory.EngineFactory(self.__bus)
        if exec_by_ibus:
            self.__bus.request_name("org.freedesktop.IBus.BogoPython", 0)
        else:
            self.__bus.register_component(self.__component)

    def run(self):
        self.__mainloop.run()

    def __bus_disconnected_cb(self, bus):
        self.__mainloop.quit()


def launch_engine(exec_by_ibus):
    IMApp(exec_by_ibus).run()

def print_help(out, v = 0):
    print >> out, "-i, --ibus             executed by ibus."
    print >> out, "-h, --help             show this message."
    print >> out, "-d, --daemonize        daemonize ibus"
    sys.exit(v)

def main():
    try:
        locale.setlocale(locale.LC_ALL, "")
    except:
        pass

    exec_by_ibus = False
    daemonize = False

    shortopt = "ihd"
    longopt = ["ibus", "help", "daemonize"]

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
        else:
            print >> sys.stderr, "Unknown argument: %s" % o
            print_help(sys.stderr, 1)

    if daemonize:
        if os.fork():
            sys.exit()

    launch_engine(exec_by_ibus)

if __name__ == "__main__":
    main()
