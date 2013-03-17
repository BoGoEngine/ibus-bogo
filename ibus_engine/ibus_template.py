#
# IBus-Censor - The Vietnamese IME for IBus
#
# Copyright (c) 2012- Long T. Dam <longdt90@gmail.com>,
#                     Trung Ngo <ndtrung4419@gmail.com>
#
# This file is part of IBus-Censor Project
# IBus-Censor is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# IBus-Censor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with IBus-Censor.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import IBus
from gi.repository import GLib
from gi.repository import GObject


def to_text(string):
    text = IBus.Text.new_from_string(string)
    text.append_attribute(IBus.AttrType.UNDERLINE,
        IBus.AttrUnderline.SINGLE, 0, len(string))
    return text


class Engine(IBus.Engine):
    __gtype_name__ = 'EngineCensor'

    def __init__(self):
        super(Engine, self).__init__()
        self.input = ""

    def do_process_key_event(self, key_val, key_code, state):
        is_press = (state & IBus.ModifierType.RELEASE_MASK) == 0
        if not is_press:
            return False
        
        self.forward_key_event(IBus.BackSpace, 14, 0)

        return True

    def do_enable(self):
        print("Enabled")

    def do_disable(self):
        print("Disabled")


class IMApp:
    def __init__(self, exec_by_ibus):
        self.__id = 0
        engine_name = "Censor Engine"
        self.__component = \
          IBus.Component.new("org.freedesktop.IBus.CensorPython",
                             "Censor Engine for IBus",
                             "0.2",
                             "GPLv3",
                             "Long T. Dam <longdt90@gmail.com>",
                             "https://github.com/CensorEngine/ibus-censor",
                             "/usr/bin/exec",
                             "ibus-censor")
        engine = IBus.EngineDesc(name="censor")
        self.__component.add_engine(engine)
        self.__mainloop = GObject.MainLoop()
        self.__bus = IBus.Bus()
        self.__bus.connect("disconnected", self.__bus_disconnected_cb)
        self.__factory = IBus.Factory.new(self.__bus.get_connection())
        self.__factory.add_engine("censor",
                GObject.type_from_name("EngineCensor"))
        if exec_by_ibus:
            self.__bus.request_name("org.freedesktop.IBus.CensorPython", 0)
        else:
            self.__bus.register_component(self.__component)
            self.__bus.set_global_engine_async(
                    "censor", -1, None, None, None)

    def run(self):
        self.__mainloop.run()

    def __bus_disconnected_cb(self, bus):
        self.__mainloop.quit()


def main():
    IBus.init()
    IMApp(False).run()

if __name__ == "__main__":
    main()
