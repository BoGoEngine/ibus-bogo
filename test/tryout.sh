#!/bin/sh

TEST_DIR=$(cd `dirname $0`; pwd)
ENGINE_DIR=$TEST_DIR/../engine/

pkill -f "ibus-bogo"
python3 $ENGINE_DIR/main.py
