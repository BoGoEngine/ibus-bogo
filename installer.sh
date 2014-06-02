#!/bin/bash
set -o nounset

RED="\e[1;31m"
RESET="\e[0m"


[ ! -f /etc/os-release ] &&
	echo -e $RED"Không thể xác định bản phân phối của bạn." \
	            "Vui lòng kiểm tra /etc/os-release."$RESET &&
	exit 1

source /etc/os-release

# Prefer the $ID_LIKE variable from os-release. e.g. Elementary OS or Mint
# will be treated as Ubuntu.
DISTRO=${ID_LIKE:-$ID}
# Archlinux and Debian unstable don't have VERSION_ID
DISTRO_VERSION=${VERSION_ID:-''}
BASE=~/.local/share/ibus-bogo
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

# A mapping between $DISTRO and install_ function postfix
declare -A SUPPORTED_DISTRO=(["arch"]="arch" ["debian"]="debian" ["ubuntu"]="debian")


[ ! ${SUPPORTED_DISTRO["$DISTRO"]} ] &&
	echo $RED"Xin lỗi. Bản phân phối của bạn không được hỗ trợ."$RESET &&
	exit 1

print_info() {
	echo -e $RED"$1"$RESET
}

install_debian () {
	dpkg --status ibus-bogo > /dev/null 2>&1
	if [ $? -eq 0 ]
	then
		print_info "# Gỡ cài đặt ibus-bogo..."
		sudo apt-get remove ibus-bogo --assume-yes
		[ $? -ne 0 ] && exit 1
	fi

	DEPS='git ibus python3 python3-gi gir1.2-ibus-1.0 python3-pyqt4 libnotify4 gir1.2-notify-0.7 python3-enchant'
	dpkg --status $DEPS > /dev/null 2>&1
	if [ $? -ne 0 ]
	then
		print_info "\# Cài đặt phần mềm phụ thuộc..."
		sudo apt-get install $DEPS --assume-yes || exit 1
	fi

	install_bogo
}

install_arch () {
	DEPS="ibus python python-gobject python-pyqt4 libnotify qt4 git python-pyenchant hunspell-en"
	sudo pacman -Q ibus-bogo > /dev/null 2>&1
	if [ $? -eq 0 ]
	then
		print_info "# Gỡ cài đặt ibus-bogo..."
		sudo pacman -R ibus-bogo --noconfirm
	fi

	print_info "# Cài đặt phần mềm phụ thuộc..."
	sudo pacman -S $DEPS --noconfirm || exit 1
	install_bogo
}

install_bogo () {
	print_info "# Đang tải ibus-ringo về $BASE..."
	[ ! -d $BASE ] && git clone $REPO $BASE
	cd $BASE

	git reset --hard HEAD
	git pull
	git submodule init
	git submodule update

	# make sure /home/$SUDO_USER/.local/share/applications exists...
	mkdir -p ~/.local/share/applications

	# FIXME: This is duplicated from gui/ibus-setup-bogo.desktop
	ENTRY="\
[Desktop Entry]\n
Encoding=UTF-8\n
Name=BoGo Settings (unstable)\n
Comment=Settings for the ibus-bogo the Vietnamese input method\n
Exec=python3 ${BASE}/gui/controller.py\n
Icon=ibus-bogo\n
Type=Application\n
Categories=Utility;\n"

	echo -e $ENTRY > ~/.local/share/applications/ibus-bogo-setup.desktop

	sudo cp $BASE/ibus_engine/data/bogo.xml /usr/share/ibus/component &&
	sudo sed -i \
	         -e "s|@EXEC_PATH@|${BASE}/launcher.sh|g" \
	         -e "s|@ICON_PATH@|${BASE}/ibus_engine/data/ibus-bogo-dev.svg|g" \
	         -e "s|@SETUP_PATH@|python3 ${BASE}/gui/controller.py|g" \
		 /usr/share/ibus/component/bogo.xml

	if [ $? -ne 0 ]
	then
		rm -r $BASE
		rm ~/.local/share/applications/ibus-setup-bogo.desktop
		exit 1
	fi

	print_info "# Đang khởi động lại ibus..."
	ibus-daemon --xim --daemonize --replace
}

echo "$LICENSE" | more
install_${SUPPORTED_DISTRO["$DISTRO"]}

print_info "# Đã cài đặt thành công\n"
echo "Cảm ơn bạn đã dùng thử bộ gõ của chúng tôi!"
echo "Hãy làm theo hướng dẫn sau để hoàn tất cài đặt:"
echo "http://ibus-bogo.readthedocs.org/en/latest/install.html#cau-hinh-sau-khi-cai-dat"
