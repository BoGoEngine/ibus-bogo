#!/bin/bash
set -o nounset

RED="\e[1;31m"
RESET="\e[0m"

[ $EUID -ne 0 ] && 
	echo -e $RED"Bạn cần chạy bộ cài đặt này với lệnh sudo."$RESET &&
	exit 1

[ ! -f /etc/os-release ] &&
	echo -e $RED"Không thể xác định bản phân phối của bạn." \
	            "Vui lòng kiểm tra /etc/os-release."$RESET &&
	exit 1

source /etc/os-release

DISTRO=$NAME
DISTRO_VERSION=${VERSION_ID:-''}  # Archlinux and Debian unstable 
                                  # don't have VERSION_ID, fallback to ''
BASE=/home/$SUDO_USER/.local/share/ibus-bogo
REPO=https://github.com/lewtds/ibus-ringo

LICENSE='Xin chào, đây là bộ cài đặt ibus-ringo, một phần mềm tự do nguồn mở.
Để sử dụng, bạn cần đồng ý với những điều khoản sau.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
'

declare -A SUPPORTED_DISTRO=(["Arch Linux"]="arch" ["Debian GNU/Linux"]="debian" ["Ubuntu"]="ubuntu")

[ ! ${SUPPORTED_DISTRO["$DISTRO"]} ] &&
	echo $RED"Xin lỗi. Bản phân phối của bạn không được hỗ trợ."$RESET &&
	exit 1

[ "$DISTRO" = "Ubuntu" ] && DISTRO="Debian GNU/Linux"

print_info() {
	echo -e $RED"$1"$RESET
}

install_debian () {
	dpkg --status ibus-bogo > /dev/null 2>&1
	if [ $? -eq 0 ]
	then
		print_info "# Gỡ cài đặt ibus-bogo..."
		apt-get remove ibus-bogo --assume-yes
		[ $? -ne 0 ] && exit 1
	fi

	DEPS='git ibus python3 python3-gi gir1.2-ibus-1.0 gir1.2-wnck-3.0 python3-pyqt4 libnotify4 gir1.2-notify-0.7 python3-enchant'
	dpkg --status $DEPS > /dev/null 2>&1
	if [ $? -ne 0 ]
	then
		print_info "\# Cài đặt phần mềm phụ thuộc..."
		apt-get install $DEPS --assume-yes|| exit 1
	fi

	install_bogo
}

install_arch () {
	DEPS="ibus python python-gobject libwnck3 python-pyqt4 libnotify qt4 git python-pyenchant"
	pacman -Q ibus-bogo > /dev/null 2>&1
	if [ $? -eq 0 ]
	then
		print_info "# Gỡ cài đặt ibus-bogo..."
		pacman -R ibus-bogo --noconfirm
	fi

	print_info "# Cài đặt phần mềm phụ thuộc..."
	pacman -S $DEPS --noconfirm || exit 1
	install_bogo
}

install_bogo () {
	print_info "# Đang tải ibus-ringo về $BASE..."
	[ ! -d $BASE ] && sudo -u $SUDO_USER git clone $REPO $BASE
	cd $BASE

	sudo -u $SUDO_USER git reset --hard HEAD
	sudo -u $SUDO_USER git pull
	sudo -u $SUDO_USER git submodule init
	sudo -u $SUDO_USER git submodule update

	# make sure /home/$SUDO_USER/.local/share/applications exists...
	sudo -u $SUDO_USER mkdir -p /home/$SUDO_USER/.local/share/applications

	# FIXME: This is duplicated from gui/ibus-setup-bogo.desktop
	ENTRY="[Desktop Entry]\n
	Encoding=UTF-8\n
	Name=BoGo Settings (unstable)\n
	Comment=Settings for the ibus-bogo the Vietnamese input method\n
	Exec=python3 ${BASE}/gui/controller.py\n
	Icon=ibus-bogo\n
	Type=Application\n
	Categories=Utility;\n"

	echo -e $ENTRY | sudo -u $SUDO_USER tee /home/$SUDO_USER/.local/share/applications/ibus-bogo-setup.desktop > /dev/null

	cp $BASE/ibus_engine/data/bogo.xml /usr/share/ibus/component && sed -i "s|<exec>/usr/lib/ibus-bogo/ibus-engine-bogo --ibus</exec>|<exec>${BASE}/launcher.sh --ibus</exec>|" /usr/share/ibus/component/bogo.xml

	if [ $? -ne 0 ]
	then
		rm -r $BASE
		rm /home/$SUDO_USER/.local/share/applications/ibus-setup-bogo.desktop
		exit 1
	fi

	print_info "# Đang khởi động lại ibus..."
	sudo -u $SUDO_USER ibus-daemon --xim --daemonize --replace
}

echo "$LICENSE" | more
install_${SUPPORTED_DISTRO["$DISTRO"]}

print_info "# Đã cài đặt thành công\n"
echo "Cảm ơn bạn đã dùng thử bộ gõ của chúng tôi!"
echo "Hãy làm theo hướng dẫn sau để hoàn tất cài đặt:"
echo "http://ibus-bogo.readthedocs.org/en/latest/install.html#cau-hinh-sau-khi-cai-dat"

