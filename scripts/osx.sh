#!/bin/bash
set -ev
#pyenv global system 3.6
pyenv versions
pip3 install --upgrade pip
pip3 install pylint
pip3 install -r requirements.txt
pip3 install -r requirements-osx.txt
python3 setup.py install
