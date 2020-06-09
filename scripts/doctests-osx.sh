#!/bin/bash
set -ev
python3 -m doctest doctests/contexts-osx.txt
python3 -m doctest doctests/composer-osx.txt
#python3 -m doctest doctests/string-osx.txt
