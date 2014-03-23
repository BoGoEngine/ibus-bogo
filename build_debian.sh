#!/bin/bash

apt-get install --yes build-essential cmake devscripts debhelper python3-pyqt4 qt4-linguist-tools pyqt4-dev-tools

# Produces something like this: 0.2.99+beta2+15+gf41910e
# This would be assembled from: <latest tag>+<number of commits from that tag>+g<sha>
version=$(LC_ALL=C git describe --tags 2> /dev/null | sed -e 's/-/+/g' -e 's/^v//')

# ensure correct directory
test -r debian/control || exit 1

rm debian/changelog.dch
mv debian/changelog debian/changelog.old
echo $version > snapshot_version
dch --create --empty --package "ibus-bogo" -v "${version}" --force-distribution --distribution "unstable" "Daily build"

debuild -us -uc "$@"
rm -f snapshot_version
rm -f debian/changelog
mv debian/changelog.old debian/changelog
