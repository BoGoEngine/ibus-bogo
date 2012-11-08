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

from gi.repository import IBus, GLib

class Config:
    charset_list = ['UTF8', 'TCVN3']
    method_list = ['STelex', 'VNI']
    
    def __init__(self):
        self.__init_props()

    def __init_charset_prop_menu(self):
        charset_prop_list = IBus.PropList()
        for charset in Config.charset_list:
            charset_prop_list.append(
                IBus.Property(key = charset,
                              prop_type = IBus.PropType.RADIO,
                              label = IBus.Text.new_from_string(charset),
                              icon = '',
                              tooltip = IBus.Text.new_from_string(charset),
                              sensitive = True,
                              visible = True,
                              state = IBus.PropState.CHECKED if charset == "UTF8" else IBus.PropState.UNCHECKED,
                              sub_props = None))

        charset_prop_menu = IBus.Property(
            key = "charset",
            prop_type = IBus.PropType.MENU,
            label = IBus.Text.new_from_string("Charset"),
            icon = None,
            tooltip = IBus.Text.new_from_string("Choose charset"),
            sensitive = True,
            visible = True,
            state = IBus.PropState.UNCHECKED,
            sub_props = charset_prop_list)
        return charset_prop_menu

    def __init_method_prop_menu(self):
        method_prop_list = IBus.PropList()
        for method in Config.method_list:
            method_prop_list.append(
                IBus.Property(key = method,
                              prop_type = IBus.PropType.RADIO,
                              label = IBus.Text.new_from_string(method),
                              icon = None,
                              tooltip = IBus.Text.new_from_string(method),
                              sensitive = True,
                              visible = True,
                              state = IBus.PropState.CHECKED if method == "STelex" else IBus.PropState.UNCHECKED,
                              sub_props = None))

        method_prop_menu = IBus.Property(
            key = "method",
            prop_type = IBus.PropType.MENU,
            label = IBus.Text.new_from_string("Typing Method"),
            icon = None,
            tooltip = IBus.Text.new_from_string("Choose typing method"),
            sensitive = True,
            visible = True,
            state = IBus.PropState.UNCHECKED,
            sub_props = method_prop_list)
        return method_prop_menu

    def __init_props(self):
        self.prop_list = IBus.PropList()
        self.__charset_prop_menu = self.__init_charset_prop_menu()
        self.prop_list.append(self.__charset_prop_menu)
        self.__method_prop_menu = self.__init_method_prop_menu()
        self.prop_list.append(self.__method_prop_menu)
