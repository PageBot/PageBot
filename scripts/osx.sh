#!/bin/bash
set -ev
#pyenv global system 3.6
#pyenv versions
brew install fontconfig
pip3 install --upgrade pip
pip3 install pylint
git clone https://github.com/PageBot/PageBotCocoa.git
cd PageBotCocoa
pip3 install -r requirements.txt
cd ..
pip3 install -r requirements.txt
