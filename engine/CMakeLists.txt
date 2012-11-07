#    This file is part of IBus-BoGo project.
#    Copyright (C) Long T. Dam <longdt90@gmail.com>
#
#    IBus-BoGo is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    IBus-BoGo is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with IBus-BoGo.  If not, see <http://www.gnu.org/licenses/>.
#

install (PROGRAMS
  data/ibus-engine-bogo
  DESTINATION
  lib/bogo
  )

install (FILES
  data/bogo.xml
  DESTINATION
  ${IBUS_COMPONENT_DIR}/
  )

install (FILES
  data/ibus-bogo.svg
  DESTINATION
  ${BOGO_INSTALL_DIR}/icons/
  )

install (FILES
  main.py
  ibus_engine.py
  DESTINATION
  ${BOGO_INSTALL_DIR}
  )

install (DIRECTORY
  bogo
  DESTINATION
  ${BOGO_INSTALL_DIR}
  )
