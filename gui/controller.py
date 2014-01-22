#
# This file is part of ibus-bogo project.
#
# Copyright (C) 2012 Long T. Dam <longdt90@gmail.com>
# Copyright (C) 2012-2013 Trung Ngo <ndtrung4419@gmail.com>
# Copyright (C) 2013 Duong H. Nguyen <cmpitg@gmail.com>
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

import sys
import os
import subprocess
import logging
import json
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic
from gi.repository import Notify
import charset_converter

# Import stuff from BoGo
current_dir = os.path.dirname(__file__)

sys.path.append(os.path.abspath(os.path.join(current_dir, "..")))
sys.path.append(
    os.path.abspath(os.path.join(current_dir, "..", "ibus_engine")))

from base_config import BaseConfig
import vncharsets
import tablemodel


CONFIG_DIR = os.path.expanduser("~/.config/ibus-bogo")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)

DEFAULT_LOCALE = "vi_VN"

# logging.basicConfig(level=logging.DEBUG)


class Settings(BaseConfig, QObject):

    """
    Watches the settings file and allows access to it as a dictionary.
    """

    # TODO: Make this thing reactive

    changed = pyqtSignal()

    def __init__(self, path):
        BaseConfig.__init__(self, CONFIG_PATH)
        # QObject.__init__()

        self.watcher = QFileSystemWatcher([os.path.dirname(path), path])
        self.watcher.fileChanged.connect(self._on_file_changed)
        self.watcher.directoryChanged.connect(self._on_file_changed)

    def _on_file_changed(self, path):
        self.read_config(path)
        self.changed.emit()


class TableProxy(QObject):

    """
    Proxy class to manage the text expansion rule editor table.
    """

    def __init__(self, tableWidget, rule_file_path):

        super(TableProxy, self).__init__()

        self.tableWidget = tableWidget
        self.rule_file_path = rule_file_path

        self.tableWidget.setColumnCount(2)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.abbrRules = {}

        try:
            with open(self.rule_file_path, "r") as f:
                rules = json.load(f)
                self.fillData(rules)
        except IOError:
            pass

        self.tableWidget.sortByColumn(0, Qt.AscendingOrder)
        tableWidget.cellChanged.connect(self.on_tableWidget_cellChanged)

    def extractRow(self, row):
        try:
            abbr = self.tableWidget.item(row, 0).text()
            expanded = self.tableWidget.item(row, 1).text()
        except AttributeError:
            abbr = ""
            expanded = ""

        return (abbr, expanded)

    def appendBlankRow(self):
        self.tableWidget.insertRow(self.tableWidget.rowCount())

    def on_tableWidget_cellChanged(self, row, col):
        abbr, expanded = self.extractRow(row)

        if abbr and expanded:
            self.abbrRules[abbr] = expanded
            self.save()

    def fillData(self, dic):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.abbrRules.update(dic)

        signalState = self.tableWidget.blockSignals(True)

        for abbr, expanded in self.abbrRules.items():
            abbrItem = QTableWidgetItem(abbr)
            expandedItem = QTableWidgetItem(expanded)

            row = self.tableWidget.rowCount()

            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, abbrItem)
            self.tableWidget.setItem(row, 1, expandedItem)

        self.tableWidget.blockSignals(signalState)
        self.save()

    def save(self):
        try:
            with open(self.rule_file_path, "w") as f:
                json.dump(self.abbrRules,
                          f,
                          indent=4,
                          ensure_ascii=False,
                          sort_keys=True)
        except IOError:
            # FIXME: Popup an error dialog here
            pass

    def deleteSelection(self):
        selectedRows = (item.row() for item in self.tableWidget.selectedItems())
        selectedRows = reversed(sorted(set(selectedRows)))

        for row in selectedRows:
            try:
                abbr, _ = self.extractRow(row)
                self.abbrRules.pop(abbr)
            except KeyError:
                pass

            self.tableWidget.removeRow(row)

        self.save()

    def toUnikeyRules(self):
        return tablemodel.toUnikeyRules(self.abbrRules)

# Multiple-inheritance approach
# http://pyqt.sourceforge.net/Docs/PyQt4/designer.html

Ui_FormClass, UiFormBase = \
    uic.loadUiType(os.path.join(current_dir, "controller.ui"))


class Window(Ui_FormClass, UiFormBase):

    """
    Main program window.
    """

    def __init__(self, app, settings):
        super(Window, self).__init__()
        self.setupUi(self)
        self.app = app
        self.settings = settings
        self.settings.changed.connect(self.refreshGui)

        if "gui-language" in settings:
            locale = settings["gui-language"]
        else:
            locale = DEFAULT_LOCALE

        self.translator = QTranslator()
        self.translator.load(os.path.join(current_dir, "locales", locale))
        app.installTranslator(self.translator)

        abbr_rule_file_path = CONFIG_DIR + "/abbr_rules.json"
        self.tableProxy = TableProxy(self.abbrTable,
                                     abbr_rule_file_path)

        def onSelectionChanged(selected, deselected):
            hasSelection = self.abbrTable.selectionModel().hasSelection()
            self.removeButton.setEnabled(hasSelection)

        self.abbrTable        \
            .selectionModel() \
            .selectionChanged \
            .connect(onSelectionChanged)

        self.logoLabel.setPixmap(QIcon.fromTheme("ibus-bogo").pixmap(48, 48))

        self.setupLanguages()
        self.refreshGui()

    @pyqtSlot()
    def on_addButton_clicked(self):
        self.tableProxy.appendBlankRow()

    @pyqtSlot()
    def on_removeButton_clicked(self):
        self.tableProxy.deleteSelection()

    @pyqtSlot()
    def on_importButton_clicked(self):
        caption = "Choose a Unikey text expansion rule file"
        fileName = QFileDialog.getOpenFileName(parent=self,
                                               caption=caption)
        if fileName:
            with open(fileName, "r") as f:
                content = f.read()
                rules = tablemodel.parseUnikeyRules(content)
                self.tableProxy.fillData(rules)

    @pyqtSlot()
    def on_exportButton_clicked(self):
        caption = "Choose a location to save expansion rule file"
        fileName = QFileDialog.getSaveFileName(parent=self,
                                               caption=caption)

        if fileName:
            with open(fileName, "w") as f:
                f.write(self.tableProxy.toUnikeyRules())

    @pyqtSlot(bool)
    def on_enableAbbrCheckBox_clicked(self, state):
        self.settings["enable-text-expansion"] = state

    @pyqtSlot()
    def on_closeButton_clicked(self):
        self.close()

    @pyqtSlot()
    def on_resetButton_clicked(self):
        self.settings.reset()

    @pyqtSlot(str)
    def on_inputMethodComboBox_activated(self, index):
        logging.debug("inputComboChanged: %s", index)
        self.settings["input-method"] = index

    @pyqtSlot(str)
    def on_charsetComboBox_activated(self, index):
        logging.debug("charsetComboChanged: %s", index)
        self.settings["output-charset"] = index

    @pyqtSlot(bool)
    def on_skipNonVNCheckBox_clicked(self, state):
        logging.debug("skipNonVNCheckBoxChanged: %s", str(state))
        self.settings["skip-non-vietnamese"] = state

    @pyqtSlot(bool)
    def on_autocapCheckBox_clicked(self, state):
        logging.debug("autocapCheckBox: %s", str(state))
        self.settings["auto-capitalize-expansion"] = state

    @pyqtSlot(int)
    def on_guiLanguageComboBox_activated(self, index):
        self.switchLanguage(self.guiLanguages[index][0])
        self.settings["gui-language"] = self.guiLanguages[index][0]

    @pyqtSlot()
    def on_convertButton_clicked(self):
        # TODO Don't always process when the button is pressed.
        clipboard = self.app.clipboard()
        mime = clipboard.mimeData()
        sourceEncoding = self.sourceCharsetCombo.currentText().lower()
        try:
            if mime.hasHtml() or mime.hasText():
                html, text = mime.html(), mime.text()
                html, text = charset_converter.convert(
                    html, text, sourceEncoding)

                new_mime = QMimeData()
                new_mime.setHtml(html)
                new_mime.setText(text)

                clipboard.setMimeData(new_mime)
                n = Notify.Notification.new(
                    "Converted", sourceEncoding + "-> utf-8", "")
            else:
                n = Notify.Notification.new(
                    "Cannot convert",
                    "No HTML/plain text data in clipboard.",
                    "")
        except UnicodeEncodeError:
            n = Notify.Notification.new(
                "Cannot convert", "Mixed Unicode in clipboard.", "")
        n.show()

    @pyqtSlot()
    def on_helpButton_clicked(self):
        subprocess.call(
            "xdg-open http://ibus-bogo.readthedocs.org/en/latest/usage.html",
            shell=True)

    def switchLanguage(self, locale):
        logging.debug("switchLanguage: %s", locale)
        if locale == "en_US":
            self.app.removeTranslator(self.translator)
        else:
            self.app.removeTranslator(self.translator)
            self.translator.load(os.path.join(current_dir, "locales", locale))
            self.app.installTranslator(self.translator)

    def setupLanguages(self):
        self.guiLanguages = [
            ("en_US", "English (US)"),
            ("vi_VN", "Vietnamese")
        ]

        self.guiLanguageComboBox.clear()
        for index, lang in enumerate(self.guiLanguages):
            self.guiLanguageComboBox.insertItem(
                index,
                QIcon(os.path.join(current_dir, "locales", lang[0] + ".png")),
                lang[1])

        languages = [langTuple[0] for langTuple in self.guiLanguages]
        if "gui-language" in self.settings:
            index = languages.index(self.settings["gui-language"])
        else:
            index = languages.index(DEFAULT_LOCALE)
        self.guiLanguageComboBox.setCurrentIndex(index)

    def refreshGui(self):
        logging.debug("Refreshing GUI")

        inputMethodList = list(self.settings["default-input-methods"].keys())
        if "custom-input-methods" in self.settings:
            inputMethodList += list(self.settings["custom-input-methods"].keys())

        charsetList = [
            "utf-8",
            "tcvn3",
            "vni"
        ]

        # Set the combo boxes' initial values
        self.inputMethodComboBox.clear()
        for i in range(len(inputMethodList)):
            self.inputMethodComboBox.insertItem(i, inputMethodList[i])

        self.charsetComboBox.clear()
        for i in range(len(charsetList)):
            self.charsetComboBox.insertItem(i, charsetList[i])
            if charsetList[i] != "utf-8":
                self.sourceCharsetCombo.insertItem(i, charsetList[i].upper())

        self.inputMethodComboBox.setCurrentIndex(
            inputMethodList.index(self.settings["input-method"]))

        self.charsetComboBox.setCurrentIndex(
            charsetList.index(self.settings["output-charset"]))

        self.skipNonVNCheckBox.setChecked(
            self.settings["skip-non-vietnamese"])

        if "gui-language" in self.settings:
            self.switchLanguage(self.settings["gui-language"])

        if "auto-capitalize-expansion" in self.settings:
            self.autocapCheckBox \
                .setChecked(self.settings["auto-capitalize-expansion"])

        if "enable-text-expansion" in self.settings:
            isEnabled = self.settings["enable-text-expansion"]
            self.enableAbbrCheckBox \
                .setChecked(isEnabled)

            self.autocapCheckBox.setEnabled(isEnabled)
            self.ruleEditorGroupBox.setEnabled(isEnabled)

    def retranslateUi(self, object):
        super(Window, self).retranslateUi(object)

        self.abbrTable.setHorizontalHeaderLabels([
            QCoreApplication.translate("TableProxy", "Expand", "Text expansion"),
            QCoreApplication.translate("TableProxy", "To", "Text expansion")])

        infoLabelText = self.infoLabel.text()
        self.infoLabel.setText(infoLabelText.format(version="0.4"))

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.retranslateUi(self)


def main():
    vncharsets.init()
    Notify.init("IBus BoGo Settings")
    app = QApplication(sys.argv)

    settings = Settings(CONFIG_PATH)

    win = Window(app, settings)
    win.show()

    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app.exec_()


if __name__ == '__main__':
    main()
