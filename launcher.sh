#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

if [ $1 == "--ibus" ]
then
	# Update the installation
	#
	# ATTENTION: This command will delete all your local changes.
	git reset --hard HEAD
	git pull

	python3 ibus_engine/main.py --ibus
else
	python3 ibus_engine/main.py
fi


