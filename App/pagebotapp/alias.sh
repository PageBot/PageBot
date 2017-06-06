#!/bin/bash
#
# Script to clean and build application.
#
python setup.py py2app -A # Compile with aliased dependencies
killall PageBotApp # Kills running application.
./dist/PageBotApp.app/Contents/MacOS/PageBotApp # Calls application binary from the command line.
