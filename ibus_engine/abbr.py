from gi.repository import Gio, GObject
import json


class AbbreviationExpander():

    def __init__(self, config):
        self.config = config
        self.parse_abbr_rule()

        # Setup automatic refreshing
        f = Gio.File.new_for_path(self.config["abbreviation-rules-path"])
        self.monitor = f.monitor_file(0, None)
        self.monitor.connect("changed", self.on_file_changed)

    def on_file_changed(self, monitor, file, other_file, event_type):
        if event_type == Gio.FileMonitorEvent.CHANGES_DONE_HINT:
            self.parse_abbr_rule()

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

    def parse_abbr_rule(self):
        with open(self.config["abbreviation-rules-path"], "r") as rule_file:
            rules = json.loads(rule_file.read())
            # FIXME: some validation needed, perhaps?
            self.abbr_rules = rules
