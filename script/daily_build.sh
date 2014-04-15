#!/bin/sh

# Adapted from github/error454/mplayer-webos

# wrapper around dpkg-buildpackage to generate correct changelog
# use "debian/daily-build.sh -b" to create binary packages
# and "debian/daily-build.sh -S" to create a source package only
#

# Produces something like this: 0.2.99+beta2+15+gf41910e
# This would be assembled from: <latest tag>+<number of commits from that tag>+g<sha>
version=$(LC_ALL=C git describe --tags 2> /dev/null | sed -e 's/-/+/g' -e 's/^v//')

# Hard-coded, change to suit your path
REPOPATH="/home/chin/bogoengine.github.com/debian/unstable"

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

# Send the new .deb and .dsc to the repo at bogoengine.github.com/debian/unstable

reprepro -Vb $REPOPATH includedeb unstable ../ibus-bogo_${version}_all.deb
reprepro -Vb $REPOPATH includedsc unstable ../ibus-bogo_${version}.dsc

WORKINGDIR=`pwd`

cd $REPOPATH

git add .
git commit -a -m "Daily build ${version}"
git push

cd $WORKINGDIR
