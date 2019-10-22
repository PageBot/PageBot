#!/bin/bash
set -ev
#pyenv global system 3.6
pyenv versions
pip3 install --upgrade pip
pip3 install pylint
git clone git@github.com:PageBot/PageBotCocoa.git
cd PageBotCocoa
pip3 install -r requirements.txt
cd ..
pip3 install -r requirements.txt
