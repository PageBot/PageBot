#!/bin/bash
# https://docs.travis-ci.com/user/multi-os/

if [ $TRAVIS_OS_NAME = 'linux' ]; then
    echo python --version
    #sudo apt-get python3 python3-setuptools python3-pip
fi

