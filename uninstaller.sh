#!/bin/bash

BASE=~/.local/share/ibus-bogo

rm -rf $BASE
rm -rf ~/.local/share/applications/ibus-bogo-setup.desktop
gksudo "rm -rf /usr/share/ibus/component/bogo.xml"
ibus-daemon --xim --daemonize --replace
