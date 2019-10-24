#!/bin/bash
set -ev
python3 -m doctest -v doctests/contexts-osx.txt
python3 -m doctest -v doctests/composer-osx.txt
