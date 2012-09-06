cmake_minimum_required (VERSION 2.6)
project (IBus-Bogo)

# Author and software info:
set (AUTHORS "Long T. Dam")
set (EMAIL "longdt90@gmail.com")
set (VENDOR "Hanoi Community Space")
set (HOMEPAGE "https://github.com/milkycoffee/ibus-bogo")

# Default install prefix
set (CMAKE_INSTALL_PREFIX "/usr")

# Installation variables
set (BOGO_INSTALL_DIR "/usr/share/ibus-bogo")
set (IBUS_COMPONENT_DIR "/usr/share/ibus/component")

# Directories with CMakeLists.txt
add_subdirectory (engine)
add_subdirectory (BoGoEngine)
