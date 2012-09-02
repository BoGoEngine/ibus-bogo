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

import ibus
import BogoEngine

class EngineFactory(ibus.EngineFactoryBase):
    def __init__(self, bus):
        self.__bus = bus
        super(EngineFactory, self).__init__(self.__bus)

        self.__id = 0

    def create_engine(self, engine_name):
        print engine_name
        if engine_name == "bogo-python":
            self.__id += 1
            return BogoEngine.Engine(self.__bus,
                                     "%s/%d" % ("/org/freedesktop/IBus/BogoPython/BogoEngine", self.__id))

        return super(EngineFactory, self).create_engine(engine_name)
