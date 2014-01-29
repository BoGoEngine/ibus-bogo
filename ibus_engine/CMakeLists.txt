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

install (PROGRAMS
  data/ibus-engine-bogo
  DESTINATION
  lib/ibus-bogo
  )

install (FILES
  data/bogo.xml
  DESTINATION
  ${IBUS_COMPONENT_DIR}
  )

install (FILES
  data/ibus-bogo.svg
  DESTINATION
  share/icons/hicolor/scalable/apps
  )

install (FILES
  main.py
  ibus_engine.py
  config.py
  base_config.py
  keysyms_mapping.py
  mouse_detector.py
  abbr.py
  focus_tracker.py
  DESTINATION
  ${BOGO_INSTALL_DIR}/ibus_engine
  )

# install (FILES
#   data/default_config.json
#   DESTINATION
#   ${BOGO_INSTALL_DIR}/ibus_engine/data
# )

install (DIRECTORY
  libs
  DESTINATION
  ${BOGO_INSTALL_DIR}/ibus_engine
)

