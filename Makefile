PREFIX = /usr
APP_ROOT = $(DESTDIR)$(PREFIX)/share/ibus-bogo
IBUS_ROOT = $(DESTDIR)$(PREFIX)/share/ibus

all:


run:
	python3 ibus_engine/main.py

install:
	# TODO: More fine-grain copying
	mkdir --parent $(APP_ROOT)
	cp -rf ibus_engine gui vncharsets bogo-python $(APP_ROOT)
	mkdir --parent $(IBUS_ROOT)/component/
	cp ibus_engine/data/bogo.xml $(IBUS_ROOT)/component/
	sed -i \
                 -e "s|@EXEC_PATH@|python3 $(APP_ROOT)/ibus_engine/main.py|g" \
                 -e "s|@ICON_PATH@|${APP_ROOT}/ibus_engine/data/ibus-bogo-dev.svg|g" \
                 -e "s|@SETUP_PATH@|python3 ${APP_ROOT}/gui/controller.py|g" \
                 $(IBUS_ROOT)/component/bogo.xml


uninstall:
	rm -rf $(APP_ROOT)
	rm -rf $(IBUS_ROOT)/component/bogo.xml

test:
	# TODO: Some systems have nosetests, nosetests3.
	nosetests3

deb:
	script/build_debian.sh

.PHONY: all run install uninstall test deb
