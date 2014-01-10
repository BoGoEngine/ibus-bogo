from gi.repository import Gio
import json


class AbbreviationExpander():

    def __init__(self, config=None):
        if config:
            self.config = config
        else:
            self.config = {
                "auto-capitalize-expansion": False
            }
        self.abbr_rules = {}

    def watch_file(self, file_path):
        self.read_file(file_path)

        # Setup automatic refreshing
        self.file_path = file_path

        f = Gio.File.new_for_path(file_path)
        self.monitor = f.monitor_file(0, None)
        self.monitor.connect("changed", self.on_file_changed)

    def read_file(self, file_path):
        try:
            with open(file_path) as f:
                json_content = f.read()
                self.abbr_rules = json.loads(json_content)
        except FileNotFoundError:
            pass

    def on_file_changed(self, monitor, watched_file, other_file, event_type):
        if event_type == Gio.FileMonitorEvent.CHANGED:
            self.read_file(watched_file.get_path())

    def add_rule(self, abbreviated_string, full_string):
        self.abbr_rules[abbreviated_string] = full_string

    def expand(self, abbr_word):
        if self.config["auto-capitalize-expansion"]:
            abbr_word_lower = abbr_word.lower()

            if abbr_word_lower in self.abbr_rules:
                expanded_word = self.abbr_rules[abbr_word_lower]

                if abbr_word.isupper():
                    expanded_word = expanded_word.upper()
                elif abbr_word.istitle() and expanded_word.islower():
                    expanded_word = expanded_word.capitalize()

                return expanded_word
            # if a lower case match is not found then
            # fallback to a normal case match
        
        if abbr_word in self.abbr_rules:
            return self.abbr_rules[abbr_word]
        else:
            return abbr_word
