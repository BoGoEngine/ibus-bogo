# vim: set expandtab softtabstop=4 shiftwidth=4:
from gi.repository import Gtk

class TrayIcon:
    def __init__(self):
        self.icon = Gtk.StatusIcon()
        self.enable()

    def disable(self):
        self.icon.set_from_icon_name("ibus")

    def enable(self):
        self.icon.set_from_icon_name("ibus-bogo")

    def hide(self):
        self.icon.set_visible(False)

    def show(self):
        self.icon.set_visible(True)

