from gi.repository import Gio, GObject
import json


class AbbreviationExpander():

    def __init__(self, config):
        self.file_path = config["abbreviation-rules-path"]
        self.parse_abbr_rule()

        # Setup automatic refreshing
        f = Gio.File.new_for_path(self.file_path)
        self.monitor = f.monitor_file(0, None)
        self.monitor.connect("changed", self.on_file_changed)

    def on_file_changed(self, monitor, file, other_file, event_type):
        if event_type == Gio.FileMonitorEvent.CHANGES_DONE_HINT:
            self.parse_abbr_rule()

    def expand(self, abbr_word):
        if abbr_word in self.abbr_rules:
            return self.abbr_rules[abbr_word]
        else:
            return abbr_word

    def parse_abbr_rule(self):
        with open(self.file_path, "r") as rule_file:
            rules = json.loads(rule_file.read())
            # FIXME: some validation needed, perhaps?
            self.abbr_rules = rules
