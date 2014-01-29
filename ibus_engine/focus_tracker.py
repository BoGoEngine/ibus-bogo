from gi.repository import Wnck
import os
import logging


class FocusTracker():

    class NoneWindow():
        def get_name(self):
            return ""

        def get_class(self):
            return -1

        def get_class_group_name(self):
            return ""

    def __init__(self):
        self.window = FocusTracker.NoneWindow()

    def on_focus_changed(self):
        screen = Wnck.Screen.get_default()
        screen.force_update()
        active_window = screen.get_active_window()

        if active_window:
            self.window = active_window
        else:
            logging.debug("Can't detect window")
            self.window = FocusTracker.NoneWindow()

    def is_in_unity_dash(self):

        def is_in_unity_desktop():
            try:
                return os.environ["XDG_CURRENT_DESKTOP"] == "Unity"
            except KeyError:
                return False

        if is_in_unity_desktop() and \
                self.window.get_window_type() == Wnck.WindowType.DOCK and \
                self.window.get_name() in ['launcher', 'unity-dash']:
            return True
        else:
            return False

    def is_in_firefox(self):
        return \
            self.window.get_class_group_name() in ["Firefox"]

    def is_in_chrome(self):
        return \
            self.window.get_class_group_name() in ["Google-chrome-unstable"]
