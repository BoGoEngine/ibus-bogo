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
  ibus-engine-bogo
  DESTINATION
  libexec
  )

install (FILES
  bogo.xml
  DESTINATION
  ${IBUS_COMPONENT_DIR}/)

install (FILES
  ibus-bogo.svg
  DESTINATION
  ${BOGO_INSTALL_DIR}/icons/)

install (FILES
  BoGoMain.py
  BoGoEngine.py
  DESTINATION
  ${BOGO_INSTALL_DIR}/
  )
