# vim: set expandtab softtabstop=4 shiftwidth=4:
from gi.repository import Gtk
import os

ENGINE_PATH = os.path.dirname(__file__)

# FIXME: hardcoded path
ICON_PATH = ENGINE_PATH + '/data/ibus-bogo-dev.svg'


class TrayIcon:
    def __init__(self):
        self.icon = Gtk.StatusIcon()
        self.enable()

    def disable(self):
        self.icon.set_from_icon_name("ibus")

    def enable(self):
        self.icon.set_from_file(ICON_PATH)

    def hide(self):
        self.icon.set_visible(False)

    def show(self):
        self.icon.set_visible(True)
