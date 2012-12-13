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

from gi.repository import IBus, GLib, GObject, Gio

class Config(GObject.GObject):
    charsets = {
        'charset.utf-8' : ('UTF-8', 'UTF-8 Unicode (Times New Roman)', 'utf-8'),
        #'tcvn3' : ('TCVN3', 'Vietnamese Standard No.3 (.VnTimes)'),
        #'vni' : ('VNI', 'VNI Encoding (VNI-Times)')
    }
    methods = {
        'im.telex' : ('Telex', 'Telex with [, ], and w.', 'telex'),
        'im.simple-telex' : ('STelex', 'Minimal Telex', 'simple-telex'),
        'im.vni' : ('VNI', 'VNI Input Method', 'vni')
    }
    
    # Read this:
    # http://python-gtk-3-tutorial.readthedocs.org/en/latest/objects.html#properties
    input_method = GObject.property(type=str)
    output_charset = GObject.property(type=str)
    spellchecking = GObject.property(type=bool, default=False)
    
    def __init__(self):
        GObject.GObject.__init__(self)
        self.__backend = Gio.Settings('org.kgcd.ibus-bogo')
        self.__backend.bind('input-method', self, 'input-method', Gio.SettingsBindFlags.DEFAULT)
        self.__backend.bind('output-charset', self, 'output-charset', Gio.SettingsBindFlags.DEFAULT)
        self.__backend.bind('spellchecking', self, 'spellchecking', Gio.SettingsBindFlags.DEFAULT)
        self.__init_props()

    # This is horrible. I know. Blame IBus.
    def __init_charset_prop_menu(self):
        charset_prop_list = IBus.PropList()
        for charset in Config.charsets:
            charset_prop_list.append(
                IBus.Property(key = charset,
                              prop_type = IBus.PropType.RADIO,
                              label = IBus.Text.new_from_string(Config.charsets[charset][0]),
                              tooltip = IBus.Text.new_from_string(Config.charsets[charset][1]),
                              sensitive = True,
                              visible = True,
                              state = IBus.PropState.CHECKED if Config.charsets[charset][2] == self.output_charset else IBus.PropState.UNCHECKED,
                              sub_props = None))

        self.__charset_prop_menu = IBus.Property(
            key = "charset",
            prop_type = IBus.PropType.MENU,
            label = IBus.Text.new_from_string(Config.charsets['charset.' + self.output_charset][0]),
            icon = None,
            tooltip = IBus.Text.new_from_string("Choose charset"),
            sensitive = True,
            visible = True,
            state = IBus.PropState.UNCHECKED,
            sub_props = charset_prop_list)
        return self.__charset_prop_menu

    def __init_method_prop_menu(self):
        method_prop_list = IBus.PropList()
        for method in Config.methods:
            method_prop_list.append(
                IBus.Property(key = method,
                              prop_type = IBus.PropType.RADIO,
                              label = IBus.Text.new_from_string(Config.methods[method][0]),
                              icon = None,
                              tooltip = IBus.Text.new_from_string(Config.methods[method][1]),
                              sensitive = True,
                              visible = True,
                              state = IBus.PropState.CHECKED if Config.methods[method][2] == self.input_method else IBus.PropState.UNCHECKED,
                              sub_props = None))

        self.__method_prop_menu = IBus.Property(
            key = "method",
            prop_type = IBus.PropType.MENU,
            label = IBus.Text.new_from_string(Config.methods['im.' + self.input_method][0]),
            icon = None,
            tooltip = IBus.Text.new_from_string("Choose typing method"),
            sensitive = True,
            visible = True,
            state = IBus.PropState.UNCHECKED,
            sub_props = method_prop_list)
        return self.__method_prop_menu

    def __init_props(self):
        self.prop_list = IBus.PropList()
        self.__charset_prop_menu = self.__init_charset_prop_menu()
        self.prop_list.append(self.__charset_prop_menu)
        self.__method_prop_menu = self.__init_method_prop_menu()
        self.prop_list.append(self.__method_prop_menu)

    def do_property_activate(self, prop_name, state):
        """Called when the user press a button on the panel (activate a property)
        """

        if prop_name in Config.methods and state == IBus.PropState.CHECKED:         
            #self.input_method = prop_name
            # For some unknown reason, GSettings property binding
            # won't work for write operation so we have to do this.            
            self.__backend.set_string('input-method', Config.methods[prop_name][2])
            t = IBus.Text.new_from_string(Config.methods[prop_name][0])
            self.__method_prop_menu.set_label(t)
            return self.__method_prop_menu

        if prop_name in Config.charsets and state == IBus.PropState.CHECKED:
            #self.output_charset = prop_name
            self.__backend.set_string('output-charset', charsets[prop_name][2])
            t = IBus.Text.new_from_string(Config.charsets[prop_name][0])
            self.__charset_prop_menu.set_label(t)
            return self.__charset_prop_menu
