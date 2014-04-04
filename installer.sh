#!/bin/bash

DISTRO=`lsb_release --short --id`
DISTRO_VERSION=`lsb_release --short --release`
BASE=~/.local/share/ibus-bogo
REPO=https://github.com/lewtds/ibus-ringo

if [ $DISTRO == 'Ubuntu' -a $DISTRO_VERSION == '14.04' ]
then
	# Check dependencies
	DEPS='git ibus python3 python3-gi gir1.2-ibus-1.0 gir1.2-wnck-3.0 python3-pyqt4 libnotify4 gir1.2-notify-0.7'
	dpkg --status $DEPS > /dev/null
	if [ $? -ne 0 ]
	then
		gksudo "apt-get install $DEPS"
	fi
fi

git clone $REPO $BASE
cd $BASE
git submodule init
git submodule update


# FIXME: This is duplicated from gui/ibus-setup-bogo.desktop
cat > ~/.local/share/applications/ibus-bogo-setup.desktop <<EOF
[Desktop Entry]
Encoding=UTF-8
Name=BoGo Settings (unstable)
Comment=Settings for the ibus-bogo the Vietnamese input method
Exec=python3 ${BASE}/gui/controller.py
Icon=ibus-bogo
Type=Application
Categories=Utility;
EOF

gksudo cp $BASE/ibus_engine/data/bogo.xml /usr/share/ibus/component/
gksudo -- sed -e "s|<exec>/usr/lib/ibus-bogo/ibus-engine-bogo --ibus</exec>|<exec>${BASE}/launcher.sh --ibus</exec>|" --in-place /usr/share/ibus/component/bogo.xml

ibus-daemon --xim --daemonize --replace
