#!/bin/bash
set -ev
# https://docs.travis-ci.com/user/multi-os/

#if [ $TRAVIS_OS_NAME = 'linux' ]; then
    #sudo apt-get python3 python3-setuptools python3-pip
#fi
python --version
#pyenv versions
#pyenv global system 3.6
pip3 install --upgrade pip
pip3 install pylint
pip3 install -r requirements.txt
