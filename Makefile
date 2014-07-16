BASE_DIR=/usr
APP_ROOT=$(BASE_DIR)/share/ibus-bogo

test:
	# TODO: Some systems have nosetests, nosetests3.
	nosetests

install:
	mkdir --parent $(APP_ROOT)
	cp -rf ibus_engine gui vncharsets bogo-python $(APP_ROOT)
	cp -rf ibus_engine/data/bogo.xml $(BASE_DIR)/share/ibus/component/
	sed -i \
                 -e "s|@EXEC_PATH@|python3 $(APP_ROOT)/ibus_engine/main.py|g" \
                 -e "s|@ICON_PATH@|${APP_ROOT}/ibus_engine/data/ibus-bogo-dev.svg|g" \
                 -e "s|@SETUP_PATH@|python3 ${APP_ROOT}/gui/controller.py|g" \
                 $(BASE_DIR)/share/ibus/component/bogo.xml


uninstall:
	rm -rf $(APP_ROOT)
	rm -rf $(BASE_DIR)/share/ibus/component/bogo.xml
