cmake_minimum_required (VERSION 2.6)
project (ibus-bogo)

list (APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)

# Author and software info:
set (AUTHORS "AUTHORS")                          # File AUTHORS
set (EMAIL "bogoengine-dev@googlegroups.com")
set (VENDOR "Hanoi Community Space")
set (HOMEPAGE "http://bogoengine.github.com/")

# IBus wouldn't detect our engine if we installed to /usr/local
# But we also have to allow other prefixes for packaging
if (CMAKE_INSTALL_PREFIX STREQUAL "/usr/local")
	message ("-- Installing to /usr by default")
	set (CMAKE_INSTALL_PREFIX "/usr")
endif()

# Installation variables
set (BOGO_INSTALL_DIR "share/ibus-bogo")
set (IBUS_COMPONENT_DIR "share/ibus/component")

# uninstall target
configure_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/cmake/cmake_uninstall.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake"
    IMMEDIATE @ONLY)

add_custom_target(uninstall
    COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake)

ENABLE_TESTING()

# Directories with CMakeLists.txt
add_subdirectory (engine)
add_subdirectory (config-gui)

