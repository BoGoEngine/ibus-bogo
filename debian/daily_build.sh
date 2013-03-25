#!/bin/sh

# Adapted from github/error454/mplayer-webos

# wrapper around dpkg-buildpackage to generate correct changelog
# use "debian/daily-build.sh -b" to create binary packages
# and "debian/daily-build.sh -S" to create a source package only
#

# Produces something like this: 0.2.99+beta2+15+gf41910e
# This would be assembled from: <latest tag>+<number of commits from that tag>+g<sha>
version=$(LC_ALL=C git describe 2> /dev/null | sed 's/-/+/g')

# ensure correct directory
test -r debian/control || exit 1

rm debian/changelog
echo $version > snapshot_version
dch --create --empty --package ibus-bogo -v ${version} --distribution "precise" "Daily build"

#dpkg-buildpackage -us -uc -i -I.svn "$@"
debuild "$@"
rm -f snapshot_version
