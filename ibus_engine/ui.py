from gi.repository import GObject
from gi.repository import IBus
from gi.repository import Gdk
import os
import subprocess


class UiDelegate():

    def __init__(self, engine):
        self.engine = engine
        self.setup_tool_buttons()

    def setup_tool_buttons(self):
        self.prop_list = IBus.PropList()

        pref_label = IBus.Text.new_from_string("Preferences")
        pref_tooltip = pref_label

        help_label = IBus.Text.new_from_string("Help")
        help_tooltip = help_label

        pref_button = IBus.Property.new(key="preferences",
                                        type=IBus.PropType.NORMAL,
                                        label=pref_label,
                                        icon="preferences-other",
                                        tooltip=pref_tooltip,
                                        sensitive=True,
                                        visible=True,
                                        state=0,
                                        prop_list=None)
        help_button = IBus.Property.new(key="help",
                                        type=IBus.PropType.NORMAL,
                                        label=help_label,
                                        icon="system-help",
                                        tooltip=help_tooltip,
                                        sensitive=True,
                                        visible=True,
                                        state=0,
                                        prop_list=None)
        self.prop_list.append(pref_button)
        self.prop_list.append(help_button)

    def do_enable(self):
        self.engine.register_properties(self.prop_list)

    def do_property_activate(self, prop_key, state):
        if prop_key == "preferences":
            try:
                pid = os.fork()
                if pid == 0:
                    # os.system("/usr/lib/ibus-bogo/ibus-bogo-settings")
                    os.system("python3 " +
                              os.path.join(os.path.dirname(__file__),
                                           "..",
                                           "gui/controller.py"))
                    os._exit(0)
            except:
                pass
        elif prop_key == "help":
            link = "http://ibus-bogo.readthedocs.org/en/latest/usage.html"
            subprocess.call("xdg-open " + link, shell=True)

        # FIXME: Is this really necessary?
        self.engine.reset_engine()
