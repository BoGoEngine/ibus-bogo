#!/bin/bash

apt-get install --yes build-essential cmake devscripts debhelper python3-pyqt4 qt4-linguist-tools pyqt4-dev-tools
debuild -us -uc
