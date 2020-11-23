#!/bin/bash
set -ev

# Installs PageBotOSX from git first so we develop against bleeding edge commits.
git clone https://github.com/PageBot/PageBotOSX.git
cd PageBotOSX
pip3 install -r requirements.txt
cd ..
pip3 install -r requirements.txt
