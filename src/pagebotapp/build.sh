#!/bin/bash
#
# Script to clean and build application.
#
# Removes build files and compiled application.
# Compiles again.
# Kills application if running.
# Calls application binary from the command line.

rm -r build dist
python setup.py py2app
killall PageBot
./dist/PageBot.app/Contents/MacOS/PageBot
