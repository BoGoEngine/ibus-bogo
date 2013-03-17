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
# GNU General Public License for more detailsself.
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
import logging
import time

from config import Config

current_path = os.path.dirname(os.path.abspath(__file__))


class Engine(IBus.Engine):
    __gtype_name__ = 'EngineBoGo'

    def __init__(self):
        super(Engine, self).__init__()
        self.surrounding = None
        self.surrounding_double_check = None

    def do_process_key_event(self, key_val, key_code, state):
        is_press = ((state & IBus.ModifierType.RELEASE_MASK) == 0)
        if not is_press:
            return False

        #print(self.get_surrounding_text()[0].get_text())
        #self.delete_surrounding_text(-1, 1)
        #print(self.get_surrounding_text()[0].get_text())
        print(self.does_surrounding())
        
        return True

    def does_surrounding(self):
        """Test if an input context really supports surrounding text
        Note that this would not work if the buffer is empty.

        Return
            True - if it does
            False - otherwise
        """
        surrounding = self.get_surrounding_text()[0].get_text()
        if not surrounding:
            return False
            # self.commit_text(IBus.Text.new_from_string("a"))
            # surrounding = self.get_surrounding_text()[0].get_text()
            # if surrounding != "a":
            #     print("deleting")
            #     self.forward_key_event(IBus.BackSpace, 14, 0)
            #     return False
            # else:
            #     print ("here")
            #     self.delete_surrounding_text(-1, 1)
            #     return True
        else:
            ch = surrounding[-1]
            print(surrounding)
            key_sent = "e" if ch == "a" else "a"
            #self.forward_key_event(ord(key_sent), 0, 0)
            self.commit_text(IBus.Text.new_from_string(key_sent))
            self.delete_surrounding_text(-1, 1)
            surrounding = self.get_surrounding_text()[0].get_text()
            if surrounding[-1] == key_sent:
                able = False
                self.forward_key_event(IBus.BackSpace, 14, 0)
            else:
                able = True
            return able

    def do_set_capabilities(self, caps):
        print(caps >> 5 & 1)

    def do_enable(self):
        print("Enabled")
        self.get_surrounding_text()
        

    def do_disable(self):
        print("Disabled")

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
                                  layout = "us")
        self.__component.add_engine(engine)
        self.__mainloop = GObject.MainLoop()
        self.__bus = IBus.Bus()
        self.__bus.connect("disconnected", self.__bus_disconnected_cb)
        self.__config = Config()
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

def print_help(out, v = 0):
    print >> out, "-i, --ibus             executed by IBus."
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
    longopt = ["ibus", "help", "daemonize",]

    try:
        opts, args = getopt.getopt(sys.argv[1:], shortopt, longopt)
    except getopt.GetoptError:
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

    if not exec_by_ibus:
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    launch_engine(exec_by_ibus)

if __name__ == "__main__":
    main()
