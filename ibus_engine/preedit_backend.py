#
# This file is part of ibus-bogo project.
#
# Copyright (C) 2014 Trung Ngo <ndtrung4419@gmail.com>
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

import logging
from gi.repository import IBus

import vncharsets
from base_backend import BaseBackend

vncharsets.init()


class PreeditBackend(BaseBackend):

    """
    Backend for Engine that tries to directly manipulate the
    currently typing text inside the application being typed in.
    """

    def __init__(self, engine, config, abbr_expander):
        self.engine = engine
        self.config = config
        self.abbr_expander = abbr_expander

    def reset(self):
        self.engine.hide_preedit_text()
        super().reset()

    def update_composition(self, string):
        logging.debug("Updating composition...")
        text = IBus.Text.new_from_string(string)
        text.append_attribute(type=IBus.AttrType.UNDERLINE,
                              value=IBus.AttrUnderline.SINGLE,
                              start_index=0,
                              end_index=len(string))

        self \
            .engine \
            .update_preedit_text_with_mode(text=text,
                                           cursor_pos=len(string),
                                           visible=True,
                                           mode=IBus.PreeditFocusMode.COMMIT)

    def commit_composition(self):
        logging.debug("Committing composition...")
        self.engine.update_preedit_text(text=IBus.Text.new_from_string(""),
                                        cursor_pos=0,
                                        visible=False)
        self.engine.commit_text(IBus.Text.new_from_string(self.editing_string))

    def process_key_event(self, keyval, modifiers):
        if keyval in [IBus.Return, IBus.BackSpace, IBus.space]:
            return self.on_special_key_pressed(keyval)

        eaten = super().process_key_event(keyval, modifiers)

        if eaten:
            self.update_composition(self.editing_string)

        return eaten

    def do_enable(self):
        pass

    def do_focus_in(self):
        pass

    def on_special_key_pressed(self, keyval):
        if keyval == IBus.Return:
            self.reset()
            return False

        if keyval == IBus.BackSpace:
            eaten = len(self.editing_string) > 0
            self.on_backspace_pressed()
            return eaten

        if keyval == IBus.space:
            self.on_space_pressed()
            self.reset()
            return False
