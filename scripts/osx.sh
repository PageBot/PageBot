#!/bin/bash
set -ev
pip3.8 install --upgrade pip
pip3.8 install pylint
# Installs PageBotOSX from git so we develop against bleeding edge commits.
git clone https://github.com/PageBot/PageBotOSX.git
cd PageBotOSX
pip3.8 install -r requirements.txt
cd ..
pip3.8 install -r requirements.txt
