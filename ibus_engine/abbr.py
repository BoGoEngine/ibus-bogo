from gi.repository import Gio
import json


class AbbreviationExpander():

    def __init__(self, config=None):
        if config:
            self.config = config
        else:
            self.config = {
                "auto-capitalize-abbreviations": False
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
        with open(file_path) as f:
            json_content = f.read()
            self.abbr_rules = json.loads(json_content)

    def on_file_changed(self, monitor, watched_file, other_file, event_type):
        if event_type == Gio.FileMonitorEvent.CHANGED:
            self.read_file(watched_file.get_path())

    def add_rule(self, abbreviated_string, full_string):
        self.abbr_rules[abbreviated_string] = full_string

    def expand(self, abbr_word):
        lookup_key = abbr_word
        if self.config["auto-capitalize-abbreviations"]:
            lookup_key = abbr_word.lower()

        if lookup_key in self.abbr_rules:
            expanded_word = self.abbr_rules[lookup_key]

            if self.config["auto-capitalize-abbreviations"]:
                if abbr_word.isupper():
                    expanded_word = expanded_word.upper()
                elif abbr_word.istitle():
                    expanded_word = expanded_word.capitalize()

            return expanded_word
        else:
            return abbr_word
