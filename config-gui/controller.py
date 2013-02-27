#!/usr/bin/env python3

import sys
import os
import logging
import hashlib
import json
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import QUiLoader

DEFAULT_LOCALE = "vi_VN"

_dirname = os.path.expanduser("~/.config/ibus-bogo/")
if not os.path.exists(_dirname):
    os.makedirs(_dirname)
config_path = os.path.join(_dirname, "config.json")

jsonData = open(config_path)
data = json.load(jsonData)
inputMethodList = list(data["default-input-methods"].keys())

if "custom-input-methods" in data:
    inputMethodList += list(data["custom-input-methods"].keys())


charsetList = [
    "utf-8",
    "tcvn3",
    "vni"
]

# logging.basicConfig(level=logging.DEBUG)

current_dir = os.path.dirname(os.path.abspath(__file__))
engine_dir = os.path.abspath(os.path.join(current_dir, "..", "engine"))

sys.path.append(engine_dir)
from base_config import BaseConfig


class Settings(BaseConfig, QObject):
    # TODO: Make this thing reactive

    changed = Signal()

    def __init__(self, path):
        BaseConfig.__init__(self, config_path)
        # QObject.__init__()

        self.fileHash = hashlib.md5(str(self.keys).encode('utf-8')).hexdigest()
        self.watcher = QFileSystemWatcher([path])
        self.watcher.fileChanged.connect(self._on_file_changed)

    def _on_file_changed(self, path):
        self.read_config(path)
        h = hashlib.md5(str(self.keys).encode('utf-8')).hexdigest()
        if h != self.fileHash:
            self.changed.emit()
            self.fileHash = h
            logging.debug("File changed")


class Window(QWidget):

    def __init__(self, app, settings):
        super(Window, self).__init__()

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

        loader = QUiLoader()
        loader.setLanguageChangeEnabled(True)
        self.win = loader.load(os.path.join(current_dir, "controller.ui"), self)
        QMetaObject.connectSlotsByName(self)

        # Define GUI items
        self.inputCombo = self.win.findChild(QComboBox, "inputMethodComboBox")
        self.charsetCombo = self.win.findChild(QComboBox, "charsetComboBox")
        self.skipNonVNCheckBox = self.win.findChild(QCheckBox, "skipNonVNCheckBox")
        self.guiLanguageComboBox = self.win.findChild(QComboBox, "guiLanguageComboBox")

        # Set their initial values
        for i in range(len(inputMethodList)):
            self.inputCombo.insertItem(i, inputMethodList[i])

        for i in range(len(charsetList)):
            self.charsetCombo.insertItem(i, charsetList[i])

        self.setupLanguages()
        self.refreshGui()

        box = QVBoxLayout()
        box.addWidget(self.win)
        self.setLayout(box)

    @Slot()
    def on_closeButton_clicked(self):
        self.close()

    @Slot()
    def on_helpButton_clicked(self):
        logging.debug("help")

    @Slot()
    def on_resetButton_clicked(self):
        self.settings.reset()

    @Slot(str)
    def on_inputMethodComboBox_activated(self, index):
        logging.debug("inputComboChanged: %s", index)
        self.settings["input-method"] = index

    @Slot(str)
    def on_charsetComboBox_activated(self, index):
        logging.debug("charsetComboChanged: %s", index)
        self.settings["output-charset"] = index

    @Slot(bool)
    def on_skipNonVNCheckBox_clicked(self, state):
        logging.debug("skipNonVNCheckBoxChanged: %s", str(state))
        self.settings["skip-non-vietnamese"] = state

    @Slot(int)
    def on_guiLanguageComboBox_activated(self, index):
        self.switchLanguage(self.guiLanguages[index][0])
        self.settings["gui-language"] = self.guiLanguages[index][0]

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
            self.guiLanguageComboBox.insertItem(index, QIcon(os.path.join(current_dir, "locales", lang[0] + ".png")), lang[1])
        if "gui-language" in self.settings:
            index = [y[0] for y in self.guiLanguages].index(self.settings["gui-language"])
        else:
            index = [y[0] for y in self.guiLanguages].index(DEFAULT_LOCALE)
        self.guiLanguageComboBox.setCurrentIndex(index)

    def refreshGui(self):
        self.inputCombo.setCurrentIndex(inputMethodList.index(self.settings["input-method"]))
        self.charsetCombo.setCurrentIndex(charsetList.index(self.settings["output-charset"]))
        self.skipNonVNCheckBox.setChecked(self.settings["skip-non-vietnamese"])
        if "gui-language" in self.settings:
            self.switchLanguage(self.settings["gui-language"])

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.setWindowTitle(self.tr("IBus BoGo Settings"))


def main():
    app = QApplication(sys.argv)

    settings = Settings(config_path)

    win = Window(app, settings)
    win.show()

    app.exec_()
    sys.exit()


if __name__ == '__main__':
    main()
