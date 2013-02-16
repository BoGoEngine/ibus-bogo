#!/usr/bin/env python2.7

import sys
import os
import logging
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import QUiLoader


# TODO: Read these lists from a config file
inputMethodList = [
    "telex",
    "simple-telex",
    "vni"
]

charsetList = [
    "utf-8",
    "tcvn3",
    "vni"
]

logging.basicConfig(level=logging.DEBUG)

_dirname = os.path.expanduser("~/.config/ibus-bogo/")
if not os.path.exists(_dirname):
    os.makedirs(_dirname)
config_path = os.path.join(_dirname, "config.json")

current_dir = os.path.dirname(os.path.abspath(__file__))
engine_dir = os.path.abspath(os.path.join(current_dir, "..", "engine"))

sys.path.append(engine_dir)
from config import BaseConfig


class Settings(BaseConfig, QObject):

    changed = Signal()

    def __init__(self, path):
        BaseConfig.__init__(self, config_path)
        # QObject.__init__()

        self.read_config()
        self.watcher = QFileSystemWatcher([path])
        self.watcher.fileChanged.connect(self._on_file_changed)

    def _on_file_changed(self, path):
        logging.debug("File changed")
        self.read_config()
        self.changed.emit()


class Window(QWidget):

    def __init__(self, app, settings):
        super(Window, self).__init__()

        self.app = app
        self.settings = settings
        self.settings.changed.connect(self.refresh_gui)

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
        self.refresh_gui()

        box = QVBoxLayout()
        box.addWidget(self.win)
        self.setLayout(box)

    @Slot()
    def on_closeButton_clicked(self):
        self.close()

    @Slot()
    def on_helpButton_clicked(self):
        print("help")

    @Slot()
    def on_resetButton_clicked(self):
        self.settings.reset()

    @Slot(unicode)
    def on_inputMethodComboBox_activated(self, index):
        logging.debug("inputComboChanged: %s", index)
        self.settings["input-method"] = index

    @Slot(unicode)
    def on_charsetComboBox_activated(self, index):
        logging.debug("charsetComboChanged: %s", index)
        self.settings["output-charset"] = index

    @Slot(int)
    def on_skipNonVNCheckBox_stateChanged(self, state):
        logging.debug("skipNonVNCheckBoxChanged: %d", state)
        self.settings["skip-non-vietnamese"] = (False, None, True)[state]

    @Slot(int)
    def on_guiLanguageComboBox_activated(self, index):
        if self.guiLanguages[index][0] == "en_US":
            self.app.removeTranslator(self.translator)
        else:
            self.app.removeTranslator(self.translator)
            self.translator.load(os.path.join(current_dir, "locales/") + self.guiLanguages[index][0])
            self.app.installTranslator(self.translator)

    def setupLanguages(self):
        self.guiLanguages = [
            ("vi_VN", self.tr("Vietnamese")),
            ("en_US", self.tr("US English"))
        ]

        self.guiLanguageComboBox.clear()
        for index, lang in enumerate(self.guiLanguages):
            self.guiLanguageComboBox.insertItem(index, QIcon(os.path.join(current_dir, "locales/") + lang[0] + ".png"), lang[1])

    def refresh_gui(self):
        self.inputCombo.setCurrentIndex(inputMethodList.index(self.settings["input-method"]))
        self.charsetCombo.setCurrentIndex(charsetList.index(self.settings["output-charset"]))
        self.skipNonVNCheckBox.setChecked(self.settings["skip-non-vietnamese"])

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.setupLanguages()


def main():
    app = QApplication(sys.argv)

    translator = QTranslator()
    translator.load(os.path.join(current_dir, "locales/vi_VN"))
    app.installTranslator(translator)

    settings = Settings(config_path)
    win = Window(app, settings)
    win.translator = translator
    win.show()

    app.exec_()
    sys.exit()


if __name__ == '__main__':
    main()
