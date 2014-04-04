#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

# Update the installation
#
# ATTENTION: This command will delete all your local changes.
git reset --hard HEAD
git pull

python3 ibus_engine/main.py

