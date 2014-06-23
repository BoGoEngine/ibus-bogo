# vim: set expandtab softtabstop=4 shiftwidth=4:
#
# This file is part of ibus-bogo project.
#
# Copyright (C) 2012 Long T. Dam <longdt90@gmail.com>
# Copyright (C) 2012-2014 Trung Ngo <ndtrung4419@gmail.com>
# Copyright (C) 2013 Duong H. Nguyen <cmpitg@gmail.com>
# Copyright (C) 2013 Hai P. Nguyen <hainp2604@gmail.com>
# Copyright (C) 2013-2014 Hai T. Nguyen <phaikawl@gmail.com>
#
# ibus-bogo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ibus-bogo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ibus-bogo.  If not, see <http://www.gnu.org/licenses/>.
#

from gi.repository import IBus, Gtk
import os
import subprocess
import logging
import enchant

#from mouse_detector import MouseDetector
from ui import UiDelegate
from preedit_backend import PreeditBackend
from surrounding_text_backend import SurroundingTextBackend
from auto_corrector import AutoCorrector

logger = logging.getLogger(__name__)

ENGINE_PATH = os.path.dirname(__file__)
DICT_PATH = ENGINE_PATH + '/data'
PWL_PATH = os.path.expanduser('~/.config/ibus-bogo/spelling-blacklist.txt')


class Engine(IBus.Engine):
    __gtype_name__ = 'EngineBoGo'

    def __init__(self, config, abbr_expander):
        super().__init__()

        self.config = config
        self.ui_delegate = UiDelegate(engine=self)

        custom_broker = enchant.Broker()
        custom_broker.set_param(
            'enchant.myspell.dictionary.path',
            DICT_PATH)

        spellchecker = enchant.DictWithPWL(
            'vi_VN_telex',
            pwl=PWL_PATH,
            broker=custom_broker)

        # FIXME: Catch enchant.errors.DictNotFoundError exception here.
        english_spellchecker = enchant.Dict('en_US')

        auto_corrector = AutoCorrector(
            config, spellchecker, english_spellchecker)

        self.preedit_backend = PreeditBackend(
            engine=self,
            config=config,
            abbr_expander=abbr_expander,
            auto_corrector=auto_corrector)

        self.surrounding_text_backend = SurroundingTextBackend(
            engine=self,
            config=config,
            abbr_expander=abbr_expander,
            auto_corrector=auto_corrector)

        # The preedit backend is the default
        self.backend = self.preedit_backend

        # Create a new thread to detect mouse clicks
        # mouse_detector = MouseDetector.get_instance()
        # mouse_detector.add_mouse_click_listener(self.reset)

        self.caps = 0

        self.vietnameseMode = True

        self.reset()

    def reset(self):
        self.backend.reset()

    def turn_on(self):
        self.vietnameseMode = True
        self.ui_delegate.do_enable()
        self.do_enable()

    def turn_off(self):
        self.vietnameseMode = False
        self.ui_delegate.do_disable()
        self.do_disable()

    # The "do_" part denotes a default signal handler
    def do_process_key_event(self, keyval, keycode, modifiers):
        """Implement IBus.Engine's process_key_event default signal handler.

        Args:
            keyval - The keycode, transformed through a keymap, stays the
                same for every keyboard
            keycode - Keyboard-dependant key code
            modifiers - The state of IBus.ModifierType keys like
                Shift, Control, etc.
        Return:
            True - if successfully process the keyevent
            False - otherwise

        This function gets called whenever a key is pressed.
        """

        # Ignore key release events
        event_is_key_press = (modifiers & (1 << 30)) == 0

        # There is a strange overflow bug with python3-gi here so the above
        # line is used instead
        # is_press = ((modifiers & IBus.ModifierType.RELEASE_MASK) == 0)

        if not event_is_key_press:
            return False

        # TODO: configurable key
        if keyval == IBus.space and \
                modifiers & IBus.ModifierType.CONTROL_MASK:
            if self.vietnameseMode:
                self.turn_off()
            else:
                self.turn_on()

            return True

        if self.vietnameseMode:
            return self.backend.process_key_event(keyval, modifiers)
        else:
            return False

    def do_enable(self):
        logger.debug("do_enable()")
        self.backend.do_enable()

    def do_disable(self):
        logger.debug("do_disable()")
        self.reset()

    def do_focus_in(self):
        logger.debug("do_focus_in()")
        self.find_focused_executable()
        self.switch_mode()
        self.backend.do_focus_in()

        if self.vietnameseMode:
            self.ui_delegate.do_enable()

    def find_focused_executable(self):
        focused_pid = subprocess.check_output(
            "xprop -id $(xprop -root | " +
            "awk '/_NET_ACTIVE_WINDOW\(WINDOW\)/{print $NF}') | " +
            "awk '/_NET_WM_PID\(CARDINAL\)/{print $NF}'",
            shell=True).decode().strip()

        self.focused_exe = os.path.realpath(
            "/proc/{0}/exe".format(focused_pid))

        logger.debug("%s focused", self.focused_exe)

    def do_reset(self):
        logger.debug("do_reset()")
        self.reset()

    def do_focus_out(self):
        logger.debug("do_focus_out()")
        self.reset()

    def do_property_activate(self, prop_key, state):
        self.ui_delegate.do_property_activate(prop_key, state)

    def do_set_capabilities(self, caps):
        logger.debug("do_set_capabilities: %s", caps)
        self.caps = caps
        self.switch_mode()

    def switch_mode(self):
        logger.debug("is_blacklisted: %s", self.is_app_blacklisted())
        if self.caps & IBus.Capabilite.SURROUNDING_TEXT and \
                not self.is_app_blacklisted():
            self.backend = self.surrounding_text_backend
        else:
            self.backend = self.preedit_backend

    def is_app_blacklisted(self):
        for exe_name in self.config["surrounding-text-blacklist"]:
            if self.focused_exe.find(exe_name) != -1:
                return True
        return False
