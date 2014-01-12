from PyQt4.QtCore import *
from PyQt4.QtGui import *
import json


class AbbreviationTableModel(QStandardItemModel):

    """
    Loads/saves abbreviation rules and presents them as a table model to be
    displayed by a QTableView.
    """

    def __init__(self, parent, rule_file_path):
        # Initialize it with two columns and zero rows
        super(AbbreviationTableModel, self).__init__(0, 2, parent)

        self.setHeaderData(0, Qt.Horizontal, "Expand")
        self.setHeaderData(1, Qt.Horizontal, "To")

        self.rule_file_path = rule_file_path
        try:
            with open(self.rule_file_path, "r") as f:
                self.abbrRules = json.load(f)
        except IOError:
            self.abbrRules = {}

        row = 0
        for abbr, expanded in self.abbrRules.items():
            self.insertRow(row)
            self.setData(self.index(row, 0), abbr)
            self.setData(self.index(row, 1), expanded)
            row += 1

        self.itemChanged.connect(self.onItemChanged)

    def extractRow(self, row):
        try:
            abbr = self.item(row, 0).text()
            expanded = self.item(row, 1).text()
            return abbr, expanded
        except AttributeError:
            return "", ""

    def onItemChanged(self, item):
        abbr, expanded = self.extractRow(item.index().row())

        if abbr != "" and expanded != "":
            self.abbrRules[abbr] = expanded
            self.save()

    def removeRow(self, row):
        try:
            abbr, _ = self.extractRow(row)

            self.abbrRules.pop(abbr)
            self.save()
        except KeyError:
            pass
        finally:
            super(AbbreviationTableModel, self).removeRow(row)

    def save(self):
        with open(self.rule_file_path, "w") as f:
            json.dump(self.abbrRules,
                      f,
                      indent=4,
                      ensure_ascii=False,
                      sort_keys=True)

    def addBlankRow(self):
        self.appendRow([QStandardItem(), QStandardItem()])

